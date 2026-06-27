    # --- Pattern 0: intro — mitochondrial bass drone, sparse SNPs ---
    pat = mod.new_pattern()
    pat[0][0] = N(I_BASS, 'C-2', MOD_FX['SPD'], 0x05)
    mt_idx = 0
    for row in range(4, 64, 4):
        if mt_idx < len(mt_snps):
            _, _, geno = mt_snps[mt_idx]
            gv = geno_val(geno)
            vol = int(0x10 + gv * 0x14)
            pat[0][row] = N(I_BASS, 'C-2', MOD_FX['VOL'], min(vol, 0x30))
            mt_idx += 2
    patterns.append(pat)

    # --- Patterns 1-4: chromosome walk — melody from SNP data ---
    total_snps = len(auto_snps)
    snp_per_pat = max(1, total_snps // 4)

    for pat_num in range(4):
        pat = mod.new_pattern()
        start = pat_num * snp_per_pat
        end = min(start + snp_per_pat, total_snps)

        # Bass: steady chromosome root note
        if start < total_snps:
            chrom, _, _ = auto_snps[start]
            root, octave, scale = chrom_to_scale(chrom)
            bass_note = f"{root}-{octave}"
            pat[0][0] = N(I_BASS, bass_note, MOD_FX['SPD'], 0x04)
            for row in range(0, 64, 8):
                pat[0][row] = N(I_BASS, bass_note, MOD_FX['VOL'], 0x18)

        # Melody: walk through SNPs
        step = max(1, (end - start) // 16)
        for i in range(16):
            idx = start + i * step
            if idx >= len(auto_snps): break
            chrom, pos, geno = auto_snps[idx]
            gv = geno_val(geno)
            root, octave, scale = chrom_to_scale(chrom)
            note = geno_to_note(gv, scale, root)

            # Ancestry harmony layer
            anc = ancestry_at(chrom, pos, regions)
            if anc:
                anc_mode, anc_transpose, _ = ancestry_to_harmony(anc)
                note_idx = NOTE_MAP[note.split('-')[0]]
                note_idx = (note_idx + anc_transpose) % 12
                note_oct = int(note.split('-')[1])
                note = f"{NOTES[note_idx]}-{note_oct}"

            vol = int(0x10 + gv * 0x14)
            row = i * 4
            pat[1][row] = N(I_PULSE, note, MOD_FX['VOL'], min(vol, 0x2C))

            # Triangle harmony pad
            if i % 3 == 0:
                harm_root = NOTE_MAP[root]
                harm_idx = (harm_root + scale_mode[gv_to_scale_idx(gv, scale_mode)]) % 12
                harm_note = f"{NOTES[harm_idx]}-{3 if gv < 1 else 4}"
                pat[2][row] = N(I_TRIANGLE, harm_note, MOD_FX['VOL'], 0x0C)

        # Percussion: SNP density spikes
        positions_in_pat = [p for _, p, _ in auto_snps[start:end]]
        if positions_in_pat:
            for row in range(2, 62, 8):
                density = snp_density(positions_in_pat, min(positions_in_pat), max(positions_in_pat))
                if density > 0.3:
                    pat[3][row] = N(I_NOISE, 'C-3', MOD_FX['VOL'], int(0x08 + density * 0x18))

        patterns.append(pat)

    # --- Pattern 5: outro — fade, mitochondrial drone returns solo ---
    pat = mod.new_pattern()
    pat[0][0] = N(I_BASS, 'C-2', MOD_FX['SPD'], 0x06)
    for row in range(0, 64, 12):
        vol = max(0x04, 0x28 - row)
        pat[0][row] = N(I_BASS, 'C-2', MOD_FX['VOL'], vol)
    # Final note — the genome's last word
    if auto_snps:
        last_chrom, last_pos, last_geno = auto_snps[-1]
        root, octave, scale = chrom_to_scale(last_chrom)
        gv = geno_val(last_geno)
        note = geno_to_note(gv, scale, root)
        pat[1][56] = N(I_PULSE, note, MOD_FX['VOL'], 0x0C)
        pat[1][60] = N(I_PULSE, note, MOD_FX['VOL'], 0x04)
    patterns.append(pat)