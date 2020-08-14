# LaTeX Problem Database Management System.

This is a template repository for setting up a problem database management system for writing assignments in LaTeX. This system allows you to maintain a global problem database in the `problems` directory, and then reference problems in your assignments. A continuous integration workflow is set up using Github Actions to automatically compile two PDF versions of each assignment (one with solutions and one without), so that only TeX files ever need to be committed to the repository, and all PDFs are automatically generated. To begin using this workflow for your own assignment development, simply create your own fork of this repository, delete the example problems and assignments, and begin adding your own.

## Overview

PDF versions of the assignments and solutions are in the `pdf` folder, while the rest of the repository only contains TeX files and assets for use in TeX files. Whenever a new change to any `.tex` file is pushed to this repository, all assignment and solution PDFs are automatically re-built and put into respective sub-directories in the `pdf` directory. There is never any reason to directly push PDF files to this repository.

Each problem in the question bank lives in its own TeX file in the problems directory, sorted by topic. Creating a new assignment from the bank is as easy as using `\import` statements in the body of the assignment to reference the TeX file for the respective problems you would like to include in the assignment. Additionally, the presence or absence of a line defining the variable `\showsolutions` in the preamble of the TeX file is what determines if the PDF will be rendered with or without solutions. This allows the auto-build script to generate both the assignment and the solutions document from the same TeX source. This way, only one TeX file needs to be pushed for any assignment. See the `homework` directory for example assignment files. For instance, the files `pdf/homework/assignments/hw_assignment.pdf` and `pdf/homework/solutions/hw_solutions.pdf` were both auto-generated from the file `homework/hw.tex`.

To add a new problem to the bank or to use a problem in a new assignment, see the instructions below.

## Adding a new problem to the question bank

To add a new problem to the question bank, create a new `.tex` file in an appropriate subdirectory of the `problems` folder. It doesn't actually matter how you organize the `problems` folder, but it is best to keep this folder organized by topic. In this new TeX file, write your new problem and its solution using the `problem` LaTeX environment defined in the `assignment.sty` style file. This TeX file should not have a preamble though, as we will later include this file in a different document which will have a preamble and will be the file that actually gets compiled. The following is the necessary syntax for using the `problem` environment to define a new problem.

```
\begin{problem}{Title of the problem}
    \question{
        Latex code for the problem statement.
    }
    \solution{
        Latex code for the solution.   
    }
\end{problem}
```

The code in both the `\question` and `\solution` sections can be any arbitrary latex code, with math environments, enumerations, or really anything else. If you want to use a command that requires a new package inclusion, you should still not put an include statement in the problem file. Instead, add it to the `assignment.sty` file instead, since this file will be included in any assignment that references our new problem file.

As an example, let us define a new problem regarding the Rodriguez rotation formula. We will create a new file `./problems/rotations/rodriguez.tex` with the following contents

```
\begin{problem}{Rodriguez' Formula}
    \question{
        Answer the following questions:
        \begin{enumerate}[(a)]
            \item Using Rodriguez' rotation formula, write down an expression for 
            $e^{\hat\omega}$ where $\omega$ is a given vector in $\mathbb R^3$.
            \item Write down an expression for a rotation matrix implementing a rotation
            by $\theta$ radians counterclockwise about an axis in the direction of 
            $\omega \in \mathbb R^3$.
        \end{enumerate}
    }
    \solution{
        \begin{enumerate}
            \item Let $\theta = ||\omega||$ and $K = \hat\omega / \theta$. Then
            \begin{align}
                e^{\hat\omega} = I + (\sin \theta) K + (1-\cos \theta) K^2
            \end{align}
            
            \item Recall that this rotation matrix is exactly the exponential 
            $e^{\hat u \theta}$ where $u$ is a unit vector in the direction of $\omega$.
            So let $u = \omega / ||\omega||$. Then the required matrix is
            \begin{align}
                \mathbf{R} = I + (\sin \theta) \hat u + (1-\cos \theta) \hat u^2
            \end{align}
        \end{enumerate}
    }
\end{problem}
```

And that's it. We are now ready to include this problem in one or more "assignment" files.

## Using your problem in a new assignment
An assignment file is just some TeX file that has a preamble which includes the `assignment.sty` file. The general assignment file looks like this

```
\documentclass[12pt]{article}
\usepackage{../assignment}

% Comment out the next line to compile without solutions.
\newcommand{\showsolutions}{}

\setlength\parindent{0pt} %% Do not touch this
\title{Example Homework Assignment} %% Assignment Title
\author{
Course XYZ}

% Set Due Date
\DTMsavedate{duedate}{2020-09-01}
\date{Due: \DTMusedate{duedate}}

\begin{document}
\maketitle

\import{/dir/containing/first/problem/}{first_problem.tex}

\import{/dir/containing/second/problem/}{second_problem.tex}

\import{/dir/containing/third/problem/}{third_problem.tex}

\end{document}
```

As you can see, the assignment file itself doesn't need to contain any problem specific LaTeX code. Instead, we simply reference the problems in the `problems` directory using `\import` statements. The `import` statement takes two arguments. The first is the path to the directory which contains the TeX file to be imported. This path should end with a `/` and should be given _relative_ to the location of the assignment file.

So, for instance, an assignment that wishes to include our example problem from the previous section would include the following line in its body

```
\import{../problems/rotations/}{rodriguez.tex}
```

#### Compiling with and without solutions 
Another salient feature of assignment files is the line `\newcommand{\showsolutions}{}`. The presence or absence of this line decides if the assignmemt will be rendered with or without solutions. If you leave this line in and compile the assignment TeX file, the resulting PDF will have solutions after every problem. On the other hand, if you comment this line out or delete it before compiling, the assignmnt PDF will be rendered without solutions. This way, both the assignment PDF and the solutions PDF can be rendered from the same TeX file. Once an assignment file is written, we can push our changes to the repository.

## PDF Autobuild
It is never necessary to push PDF files directly to this repository. This repo is configured with a continuous integration workflow which gets triggered whenever `.tex` changes are pushed to the master branch. When this happens, all `.tex` files NOT in the `problems` folder get compiled into PDFs and put into the `pdf` directory, through an automatically generated commit which will have the commit message `Autobuild PDFs`. Moreover, assignment files are compiled twice, once with and once without the `\showsolutions` flag, and so both the assignment document and the solutions document are generated whenever new changes are pushed.

In particular, the files are placed in a parallel directory tree inside the `pdf` folder. For instance, if an assignment file called `hw.tex` is placed in the directory `/path/to/dir` (given relative to the root of the repo), then the assignment PDF (without solutions) is placed in `pdf/path/to/dir/assignments` and is named `hw_assignment.pdf`, whereas the solutions PDF is placed in `pdf/path/to/dir/solutions` and is called `hw_solutions.pdf`.

This means that you should NOT push ANY files generated by a latex compiler to this repository manually -- you should only ever push `.tex` files and assets for use in `.tex` files. If you have been making changes locally and using a LaTeX compiler to test, you should delete any generated files (including PDFs) before committing.

The autobuild is implemented in the python script `compile_pdfs.py`. Take a look at that file if you would like to see exactly what is going on.

## Global Question Bank PDF
It is a good idea to keep a human-readable log of all problems in the question bank. To this end, an assignment file called `question_bank.tex` is maintained in the `question_bank` directory. Whenever you add a new problem to the bank. you should also import it into the corresonding section of this file, even if it is not immediately being used in another assignment. This helps everyone keep track of what problems are already in the bank and allows for a convenient way to browse the entire question bank, sorted by topic. As always, this file too is auto-compiled and PDFs are placed in `pdf/question_bank`.

## Enhancements TODO
1. Automatically delete PDF files whose corresponding assignment files have been deleted.
