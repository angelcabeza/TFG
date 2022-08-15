for file in *.ply; do
    meshlabserver -i "$file" -o "${file%.*}.obj"
done
