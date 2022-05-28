FILE=$1
ENGINE="pdflatex"
BIBENGINE="biber"

$ENGINE $FILE.tex
$BIBENGINE --output-safechars $FILE
$ENGINE $FILE.tex
$ENGINE $FILE.tex
