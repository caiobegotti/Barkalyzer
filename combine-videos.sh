#!/bin/bash -eu
# author: @caiobegotti
# license: MIT

which ffmpeg || (echo "Missing dependency, please install ffmpeg!"; exit 1)

output_file="output.mp4"
temp_list=$(mktemp)
echo "" > ${temp_list}

if [ "$#" -lt 1 ]; then
    echo "Usage: ${0} <video1> [<video2> ...]"
    exit 1
fi

for file in ${@}; do
    echo "file '$(realpath ${file})'" >> ${temp_list}
done

ffmpeg -f concat -safe 0 -i "${temp_list}" -c copy "${output_file}" && rm ${temp_list}

echo "Combined audios saved as ${output_file}"

exit 0