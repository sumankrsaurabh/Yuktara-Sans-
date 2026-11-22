"""Yuktara Sans v2 = Inter (SIL OFL 1.1), rebranded and re-tuned for a more geometric, open, readable look.
 - Yuktara Sans         : text cut (Inter base) with extra letter-spacing for readability
 - Yuktara Sans Display : headline cut (Inter Display base), tighter and smoother at large sizes
Edit FEATURES / TRACKING below and re-run:  python3 customize_inter.py"""
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables as ot

SRC, OUT = "/usr/share/fonts/opentype/inter", "/mnt/user-data/outputs"
FEATURES = ["cv11", "cv06", "ss03", "ss01"]
TRACKING = {"Light": 24, "Regular": 24, "Medium": 22, "SemiBold": 18, "Bold": 16, "Italic": 24, "BoldItalic": 16}
CUTS = [("Inter", "Yuktara Sans", "YuktaraSans", ["Light", "Regular", "Medium", "SemiBold", "Bold", "Italic", "BoldItalic"], True),
        ("InterDisplay", "Yuktara Sans Display", "YuktaraSansDisplay", ["Regular", "Medium", "SemiBold", "Bold"], False)]

def default_on(font, tags):
    gsub = font["GSUB"].table
    want = sorted({li for fr in gsub.FeatureList.FeatureRecord if fr.FeatureTag in tags for li in fr.Feature.LookupListIndex})
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag == "calt":
            fr.Feature.LookupListIndex = sorted(set(fr.Feature.LookupListIndex) | set(want))
            fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)

def add_tracking(font, per_glyph):
    gpos = font["GPOS"].table
    marks = {g for g, c in font["GDEF"].table.GlyphClassDef.classDefs.items() if c == 3}
    hmtx = font["hmtx"].metrics
    names = [g for g in font.getGlyphOrder() if g not in marks and g != ".notdef" and hmtx[g][0] > 0 and "space" not in g.lower()]
    st = ot.SinglePos(); st.Format = 1; st.ValueFormat = 0x0005
    st.Coverage = ot.Coverage(); st.Coverage.glyphs = names
    st.Value = ot.ValueRecord(); st.Value.XPlacement = per_glyph // 2; st.Value.XAdvance = per_glyph
    lk = ot.Lookup(); lk.LookupType = 1; lk.LookupFlag = 0; lk.SubTable = [st]; lk.SubTableCount = 1
    gpos.LookupList.Lookup.append(lk); gpos.LookupList.LookupCount = len(gpos.LookupList.Lookup)
    idx = gpos.LookupList.LookupCount - 1
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == "kern":
            fr.Feature.LookupListIndex.append(idx); fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)

def rebrand(font, src_key, family, ps):
    name = font["name"]
    for n in list(name.names):
        s, i = n.toUnicode(), n.nameID
        disp = src_key == "InterDisplay"
        if i in (1, 4, 16, 21): s = s.replace("Inter Display" if disp else "Inter", family)
        elif i in (3, 6): s = s.replace(src_key, ps)
        elif i == 5: s = s + "; Yuktara Sans 2.0"
        elif i == 0: s = "Copyright 2016 The Inter Project Authors. Modifications copyright 2026 Yuktara Tech."
        elif i == 7: s = "Yuktara Sans is derived from Inter (SIL OFL 1.1). Inter is a trademark of rsms."
        elif i == 8: s = "Yuktara Tech"
        elif i == 9: s = "Rasmus Andersson (Inter); customized by Yuktara Tech"
        elif i == 11: name.removeNames(nameID=11); continue
        else: continue
        name.setName(s, i, n.platformID, n.platEncID, n.langID)
    cff = font["CFF "].cff; td = cff.topDictIndex[0]
    cff.fontNames[0] = name.getDebugName(6); td.FullName = name.getDebugName(4); td.FamilyName = family
    td.Notice = name.getDebugName(0); font["OS/2"].achVendID = "YUKT"

for src_key, family, ps, styles, track in CUTS:
    for style in styles:
        f = TTFont(f"{SRC}/{src_key}-{style}.otf")
        default_on(f, FEATURES)
        if track: add_tracking(f, TRACKING[style])
        rebrand(f, src_key, family, ps)
        f.save(f"{OUT}/{ps}-{style}.otf"); print(f"{ps}-{style}.otf")
