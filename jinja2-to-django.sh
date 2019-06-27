function single_replace {
    python3 -c "import sys, re; print(re.sub(sys.argv[1], sys.argv[2], open(sys.argv[3]).read()))" "$@"
}

function multi_replace {
    python3 -c "import sys, re, functools; t=open(sys.argv[1]).read();
for i in range(2, len(sys.argv)-1, 2):
  t=re.sub(sys.argv[i], sys.argv[i+1], t)
print(t, end='')" "$@"
}

for file in "$@"; do
    echo Processing $file
    NEW=`python3 -c "import sys; print(sys.argv[1].split('.j2')[0], end='')" $file`

    if [[ "$NEW" == "$file" ]]; then
        NEW=$file.new
    fi;

    multi_replace $file \
        '{{ ?static\("(.*)"\) ?}}' "{% static '\1' %}" \
        "{{ ?url ?\\('(.*)'\\) ?}}" "{% url '\1' %}" \
        "{{ ?url ?\\('(.*)', ?pk=(.*)\\) ?}}" "{% url '\1' \2 %}" \
        "{% ?endblock (.*) ?%}" "{% endblock %}" \
        "{{ ?get_static_prefix ?}}" "{{ STATIC_PREFIX }}" \
        "{% ?extends '(.*).j2' ?%}" "{% extends '\1' %}" \
        "{% ?include '(.*).j2' ?%}" "{% include '\1' %}" \
        '{{ (.*) \+ " " \+ (.*) }}' '{{ \1 }} {{ \2 }}' \
        "{% ?for(.*).all\(\) ?%}" "{% for\1.all %}" \
        ".strftime\('(.*)'\)" " | date:'\1'" \
        "%Y-%m-%d-%H:%M" "Y-m-d-H:i" \
    > $NEW
    echo Exported $NEW
done
