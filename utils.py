def txt2md(path: str) :
    convert_h = { f'h{n}': '#'*n for n in range(1, 7) }
    with open(path, 'r') as file :
        lines = file.readlines()
        lines_md = []
        for line in lines :
            # 'code' -> `code`
            line = line.replace("'", "`")
            
            join = True
            texts = line.split(' ')
            # skip if text == ''
            if texts[0] :
                # h1 -> #, h2 -> ##
                if texts[0] in convert_h.keys() :
                    texts[0] = convert_h[texts[0]]

                # add width and height to ![image](path) :image microscope.png w=50 h=40
                elif texts[0] == ':image' :
                    join = False
                    dest = f'<img src="{texts[1]}"  width="{texts[2][2:]}" height="{texts[3][2:-1]}">\n'
                    line = dest

                # table
                elif texts[0] == '::' :
                    join = False
                    rows = [ row for row in line.split('::') if row ]
                    line = ''
                    line += f'|{rows[0].replace(",", "|")}|\n|--|:--:|--:|\n'
                    for row in rows[1:] :
                        row_ = f'|{row.replace(",", "|")}|\n'
                        line += row_

                # link
                elif ':a,' in line :
                    for idx, text in enumerate(texts) :
                        if text.startswith(':a,') :
                            part = text.split(',')
                            dest = f'<a href="{part[1]}" target="_blank">{part[2][:-1]}</a>\n'
                            texts[idx] = dest
                
                if join: line = ' '.join(texts)
            lines_md.append(line)

    with open(f'{path[:-4]}.md', 'w') as file :
        file.write(''.join(lines_md))

    print(f'- md: {path[:-4]}.md')
