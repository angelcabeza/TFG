for file in *.stl; do
    meshlabserver -i "$file" -o "${file%.*}.obj"
done
