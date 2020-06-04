#/bin/sh

python -m compileall .

for d in models/__pycache__; do
    for f in $d/*; do
        [[ $f =~ __pycache__/(.+).cpython-([0-9]+).pyc ]]
        echo "COPYING ${f} TO models/${BASH_REMATCH[1]}.pyc"
        cp "$f" "models/${BASH_REMATCH[1]}.pyc"
    done
done

for d in lib/__pycache__; do
    for f in $d/*; do
        [[ $f =~ __pycache__/(.+).cpython-([0-9]+).pyc ]]
        echo "COPYING ${f} TO lib/${BASH_REMATCH[1]}.pyc"
        cp "$f" "lib/${BASH_REMATCH[1]}.pyc"
    done
done

for d in __pycache__; do
    for f in $d/*; do
        [[ $f =~ __pycache__/(.+).cpython-([0-9]+).pyc ]]
        echo "COPYING ${f} TO ${BASH_REMATCH[1]}.pyc"
        cp "$f" "${BASH_REMATCH[1]}.pyc"
    done
done
