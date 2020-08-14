import os
import subprocess

def add_suffix(tex_filename, suffix):
    if tex_filename.endswith('.tex'):
        tex_filename = tex_filename[:-4] + suffix + '.tex'
    else:
        tex_filename = tex_filename + suffix
    return tex_filename

def generate_temp_tex(directory, filename):
    texfile_path = os.path.normpath(os.path.join(directory, filename))
    with open(texfile_path, 'r') as f:
        tex_lines = f.readlines()
    assignment_lines = [line for line in tex_lines if '\\showsolutions' not in line]
    assignment_code = ''.join(assignment_lines)
    solutions_lines = ['\\newcommand{\\showsolutions}{}\n'] + assignment_lines
    solutions_code = ''.join(solutions_lines)
    
    assignment_path = add_suffix(filename, '_assignment')
    with open(os.path.normpath(os.path.join(directory, assignment_path)), 'w') as f:
        f.write(assignment_code)

    solutions_path = add_suffix(filename, '_solutions')
    with open(os.path.normpath(os.path.join(directory, solutions_path)), 'w') as f:
        f.write(solutions_code)
    return assignment_path, solutions_path

def compile_and_save_tex(texfile_path, pdf_dir='pdf', compile_assignment=True, compile_solutions=True):
    directory, filename = os.path.split(texfile_path)
    save_dir_ass = os.path.normpath(os.path.join(pdf_dir, directory, 'assignments'))
    save_dir_sol = os.path.normpath(os.path.join(pdf_dir, directory, 'solutions'))
    assignment_filename, solutions_filename = generate_temp_tex(directory, filename)
    compile_pdf(directory, assignment_filename, save_dir_ass)
    compile_pdf(directory, solutions_filename, save_dir_sol)

def compile_pdf(directory, filename, move_result_to):
    """Change to dir directory and compile texfile filename, given relative to directory.
    """
    cmd = ['latexmk', '-pdf', '-dvi-', '-interaction=nonstopmode', filename]
    proc = subprocess.Popen(cmd, cwd=directory)
    proc.communicate()

    retcode = proc.returncode
    if not retcode == 0:
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

    pdf_name = filename.replace('.tex', '.pdf')
    from_file = os.path.join(directory, pdf_name)
    to_file = os.path.join(move_result_to, pdf_name)
    
    if not os.path.exists(move_result_to):
        os.makedirs(move_result_to)
    
    os.rename(from_file, to_file)

def all_non_problem_tex_files():
    def tex_files(directory):
        for subdir in os.listdir(directory):
            curr_dir = os.path.join(directory, subdir)
            if os.path.isfile(curr_dir) and curr_dir.strip().endswith('.tex'):
                yield curr_dir
            elif os.path.isdir(curr_dir) and (curr_dir != './problems'):
                yield from tex_files(curr_dir)
    yield from tex_files('.')

def main():
    for file in all_non_problem_tex_files():
        compile_and_save_tex(file)

if __name__ == '__main__':
    main()
