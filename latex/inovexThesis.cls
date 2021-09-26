\ProvidesClass{inovexThesis}
\NeedsTeXFormat{LaTeX2e}

%-------------------------------------------------------------------------------
% class options 
%-------------------------------------------------------------------------------
% title page font style
\newif\if@titlepage@sansserif
\DeclareOption{seriftitlepage}{\@titlepage@sansseriffalse}%
\DeclareOption{sansseriftitlepage}{\@titlepage@sansseriftrue}%
% title page layout lines
\newif\if@titlepage@showlayout
\DeclareOption{layouttitlepage}{\@titlepage@showlayouttrue}%
\DeclareOption{nolayouttitlepage}{\@titlepage@showlayoutfalse}%
% add toc to toc
\newif\if@addtoctotoc
\DeclareOption{addtoctotoc}{\@addtoctotoctrue}%
\DeclareOption{notocintoc}{\@addtoctotocfalse}%
% pass remaining options to scrbook class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrbook}}%
% default options
\ExecuteOptions{seriftitlepage,nolayouttitlepage,addtoctotoc}%
\ProcessOptions\relax

%-------------------------------------------------------------------------------
% derive from class scrbook 
%-------------------------------------------------------------------------------
\LoadClass[%
  a4paper,
  twoside       = true,
  fontsize      = 12pt,
  chapterprefix = false,           % don't print "Chapter XX" before chapter headings
  toc           = listof,          % include list of tables and figures in toc
  toc           = bib,             % include bib in toc
  numbers       = noenddot         % If you include an Appendix, each number will get
                                   % an ugly dot at the end, e.g. "Figure 3.9.: XXX".
                                   % This option prevents this and makes it
                                   % "Figure 3.9: XXX" as it should be
]{scrbook}%

%------------------------------------------------------------------------------
% support of UTF-8
\RequirePackage[utf8]{inputenc}
%-------------------------------------------------------------------------------

%-------------------------------------------------------------------------------
% load packages 
%-------------------------------------------------------------------------------
% use manual text positioning on title page
\if@titlepage@showlayout
  \RequirePackage[showboxes,absolute]{textpos}%
\else
  \RequirePackage[absolute]{textpos}%
\fi
% used for toc tweaking
\RequirePackage{etoolbox}%
% add toc to toc
\if@addtoctotoc
  \RequirePackage{tocbibind}%
\fi
% load color package
\RequirePackage[pgfplots,svgnames,x11names]{inovexcolor}%

%-------------------------------------------------------------------------------
% document styles
% caption style
%-------------------------------------------------------------------------------
\addtokomafont{captionlabel}{\bfseries}%
\addtokomafont{caption}{\small}%

%-------------------------------------------------------------------------------
% document properties
% parameters as set by the main file.
%-------------------------------------------------------------------------------
\newcommand{\university}[1]{\def\@university{#1}}%
\newcommand{\faculty}[1]{\def\@faculty{#1}}%
\newcommand{\degree}[1]{\def\@degree{#1}}%
\newcommand{\grade}[1]{\def\@grade{#1}}%
\newcommand{\course}[1]{\def\@course{#1}}%
\newcommand{\mail}[1]{\def\@mail{#1}}%
\newcommand{\street}[1]{\def\@street{#1}}%
\newcommand{\place}[1]{\def\@place{#1}}%
\newcommand{\matriculationnumber}[1]{\def\@matriculationnumber{#1}}%
\newcommand{\examiner}[1]{\def\@examiner{#1}}%
\newcommand{\examinermail}[1]{\def\@examinermail{#1}}%
\newcommand{\scdexaminer}[1]{\def\@scdexaminer{#1}}%
\newcommand{\scdexaminermail}[1]{\def\@scdexaminermail{#1}}%
\newcommand{\fstadvisor}[1]{\def\@fstadvisor{#1}}%
\newcommand{\fstadvisormail}[1]{\def\@fstadvisormail{#1}}%
\newcommand{\scdadvisor}[1]{\def\@scdadvisor{#1}}%
\newcommand{\scdadvisormail}[1]{\def\@scdadvisormail{#1}}%
\newcommand{\duration}[1]{\def\@duration{#1}}%

%-------------------------------------------------------------------------------
% title page sizing
%-------------------------------------------------------------------------------
% The title page is fully centered.
\def\titlepagebindingcor#1{\def\@titlepagebindingcor{#1}}
\def\@titlepagebindingcor{0mm}
\RequirePackage{calc}%
% logos
\def\logoHeight{20mm}
\def\inovexLogoWidth{28.5mm}
% Left and right margins are exactly the same.
\def\defaultwidth{150mm}%
\def\defaulthpos{30mm + \@titlepagebindingcor}%
% Vertical positions of title page entities
\def\titlevpos{100.2mm}%
\def\degreevpos{130mm}%
\def\authordatevpos{140mm}%
\def\informationvpos{170mm}%
\def\copyrightvpos{260mm}%

%-------------------------------------------------------------------------------
% font support --> requieres lato to be installed
%-------------------------------------------------------------------------------
\RequirePackage[default]{lato}
\RequirePackage[T1]{fontenc}
\fontfamily{lato}\selectfont

%-------------------------------------------------------------------------------
% robustify
%-------------------------------------------------------------------------------
% clear textpos box
% textpos interacts badly with some packages due to a conflict with \shipout
% https://tex.stackexchange.com/questions/66804/unexpected-output-using-tikz-textpos
\def\cleartextposbox{\global\setbox\TP@holdbox\vbox{}}

\AtBeginDocument{%
% pdf links: only if hyperref was loaded in main file
\@ifpackageloaded{hyperref}{%
  \hypersetup{%
    bookmarks    = true,         % show bookmarks bar?
    pdftoolbar   = true,         % show Acrobat’s toolbar?
    pdfmenubar   = true,         % show Acrobat’s menu?
    pdffitwindow = false,        % window fit to page when opened
    pdfstartview = {FitH},       % fits the width of the page to the window
    pdftitle     = {\@title},    % title
    pdfauthor    = {\@author},   % author
    pdfsubject   = {\@degree},    % subject of the document
    pdfcreator   = {\@author},   % creator of the document
    pdfnewwindow = true,         % links in new window
  }}{}%
}

%-------------------------------------------------------------------------------
% structure of title page
%-------------------------------------------------------------------------------
\renewcommand\maketitle{%
\begin{titlepage}
    % university logo
    \begin{textblock*}{\logoHeight}(9.75mm + \@titlepagebindingcor, 9.75mm)
      \noindent 
      \includegraphics[height = \logoHeight]{assets/HM_logo.png}
    \end{textblock*}
    % inovex logo
    \begin{textblock*}{\logoHeight}(\paperwidth - \inovexLogoWidth - 10mm, 10mm)
      \noindent 
      \includegraphics[height = \logoHeight]{assets/inovex_logo.pdf}
    \end{textblock*}
    % title
    \begin{textblock*}{\defaultwidth}[0,1](\defaulthpos, \titlevpos)
      \centering
      {\bfseries \Large \textcolor{inovexBlue} \@title}
      \ifdefempty{\@subtitle}{}{\vspace{1ex}\bfseries\large \@subtitle}
    \end{textblock*}
    % degree
    \begin{textblock*}{\defaultwidth}[0,1](\defaulthpos, \degreevpos)
      \centering
      {%
        \large \@degree \ in major \@course\\
        to obtain the degree \@grade
      }
    \end{textblock*}
    % author & date
    \begin{textblock*}{\defaultwidth}[0,1](\defaulthpos, \authordatevpos)
      \centering
      {submitted on \@date}
    \end{textblock*}
    % information block
    \begin{textblock*}{\defaultwidth}(\defaulthpos, \informationvpos)
      \centering
      \raggedright
        \begin{tabular}{l l}
            \textbf{Author:} & \@author, \href{mailto:\@mail}{\@mail}\\
            & \@street\\
            & \@place\\
            \textbf{Matriculationnumber:}& \@matriculationnumber\\
            \textbf{Editing time:}& \@duration \\
            \textbf{Examiner:}& \@examiner, \href{mailto:\@examinermail}{\@examinermail}\\
            \textbf{Secondary Examiner:}& \@scdexaminer, \href{mailto:\@scdexaminermail}{\@scdexaminermail}\\
            \textbf{Advisor:}& \@fstadvisor, \href{mailto:\@fstadvisormail}{\@fstadvisormail}\\
            % & \@scdadvisor, \href{mailto:\@scdadvisormail}{\@scdadvisormail}\\
            \textbf{Company:}& inovex GmbH\\
            & Lindberghstra\ss{}e 3\\
            & 80939 M\"unchen\\
        \end{tabular}
    \end{textblock*}
\end{titlepage}

% force empty page
\mbox{}
% \newpage
\thispagestyle{empty}
\null\newpage\cleartextposbox

} % end \renewcommand\maketitle

%-------------------------------------------------------------------------------
% toc tweaking
%-------------------------------------------------------------------------------
% make subsubsection numbered
\setcounter{secnumdepth}{3}

% make subsubsection appear in TOC
\setcounter{tocdepth}{3}
\endinput
