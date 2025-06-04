def split_code_with_dependencies(lines, func_defs, func_calls, max_lines=50):
    chunks = []
    total_lines = len(lines)

    for start in range(0, total_lines, max_lines):
        end = min(start + max_lines, total_lines)
        chunk = lines[start:end]

        # Find any called functions in this chunk
        called_funcs = {
            fname for fname in func_defs
            if any(fname in line for line in chunk)
        }

        required_defs = []
        for fname in called_funcs:
            if fname in func_defs:
                def_start, def_end = func_defs[fname]
                if def_end <= start:
                    required_defs += lines[def_start - 1:def_end]

        full_chunk = "\n".join(required_defs + chunk)
        chunks.append(full_chunk)

    return chunks
