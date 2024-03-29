import re


def checkForDups(tempList):  # List duplication checker
    seen = {}
    dupes = []
    for x in tempList:
        x = x.lower()
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    if str(dupes) == "[]":
        print("No Duplicates found")
    else:
        print("Duplicates found in List: " + str(dupes))


def renameFile(currentOS, filenameAndDirectory, filename, previousOutputFilename):

    # Need to be able to handle triple digits eg ep 123

    removeStrings = [  # Remove all strings listed (Note: case and order doesn't matter)
        u"\091" u"\126" u"\065" u"\065" u"\126" u"\093",  # equal to [~AA~]
        u"\126" u"\065" u"\065" u"\126",  # ~AA~
        "Diamond Edition 1080p 10bit Bluray x265 HEVC [Org DD 2.0 Hindi + DD 5.1 English] ESubs ~ TombDoc",
        "1080p 10bit Bluray x265 HEVC [Org DD 5.1 Hindi + DD 5.1 English] ESub ~ TombDoc",
        "1080p 10bit NF WEB-RIP x265 [Hindi DD 640Kbps Org 5.1 - Eng DD 2.0] ~ EmKayy",
        "[BDRip 1080p 10bit HEVC x265 Opus DualAudio(JPN ENG) Subbed Dubbed]",
        "BluRay x265 10Bit HEVC [English DD 5.1 640 Kbps] [Dzrg Torrents®]",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 Danish+Swedish Silence)",
        "1080p 10bit Bluray x265 HEVC English DDP 5.1 ESub ~ TombDoc",
        "(Dvdrip 720X480p X265 Hevc Ac3x2 2.0X2)(Dual Audio)[Sxales]",
        "[BD 2160p 4K UHD][HEVC x265 10bit][Dual-Audio][Multi-Subs]",
        "1080p NF WEBRip 10bit DD 5.1 x265.HEVC D0ct0rLew[UTR-HD]",
        "(Criterion)(1080p BluRay x265 HEVC 10bit AC3 1.0 SAMPA)",
        "Criterion (1080p BluRay x265 HEVC 10bit AAC 5.1 Tigole)",
        "(1080p DS4K RED WEB-DL x265 HEVC 10bit AAC 5.1 Vyndros)",
        "1080p BluRay x265 HEVC EAC3-SARTRE [Torrent Downloads]",
        "1080p Genuine BD Rip HEVC 2-Pass 10 Bit AC3 5.1 EN Sub",
        "[BDRip-1080p-MultiLang-MultiSub-Chapters][RiP By MaX]",
        "(1080p DSNYP Webrip x265 10bit EAC3 5.1 Atmos - Goki)",
        "(1080p DSNYP Webrip x265 10bit EAC3 5.1 - Goki)[TAoE]",
        "(1080p BluRay x265 HEVC 10bit AAC 7.1 Korean Silence)",
        "(1080p Bluray x265 HEVC 10bit AAC 5.1 Swedish Tigole)",
        "(1080p BDRip x265 10bit EAC3 5.1 - Species180) [TAoE]",
        "(1080p BluRay x265 HEVC 10bit AC3 5.1 Chinese SAMPA)",
        "(1080p ATVP Webrip x265 10bit EAC3 5.1 Atmos - Goki)",
        "[1080p x265 HEVC 10bit BD Dual Audio AAC 5.1] [Prof]",
        "2160p AMZN WEB DL AI x265 HEVC 10bit AAC 5 1 Joy UTR",
        "(1080p AMZN WEB-DL x265 HEVC 10bit EAC3 6.0 RZeroX)",
        "(1080p AMZN WEB-DL x265 HEVC 10bit DDP 5.1 Vyndros)",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 FreetheFish)",
        "(BD 1080p)(HEVC x265 10bit)(Multi-Subs)-Judas[TGx]",
        "(BD 1920x1036 x 265 10Bit 4Audio) Movie Tokuten BD",
        "(1080p BDRip x265 10bit EAC3 5.1 - xtrem3x) [TAoE]",
        "(2160p AMZN WEB-DL AI x265 HEVC 10bit AAC 5 1 Joy)",
        "(1080p AMZN WEB-DL AI x265 HEVC 10bit AAC 5 1 Joy)",
        "(1080p AMZN WEB-DL x265 HEVC 10bit AAC 2.0 Panda)",
        "(1080p BluRay x265 HEVC 10bit DTS 5.1 Qman) [UTR]",
        "(1080p BluRay x265 HEVC 10bit DTS 7.1 Qman) [UTR]",
        ".1080p.Blu-Ray.10-Bit.Dual-Audio.DTS-HD.x265-iAHD",
        "2160p NF WEBRip NVENC HEVC 10bit AAC 5 1 Joy UTR",
        "2160p AMZN WEB DL AI x265 HEVC 10bit AAC 5 1 Joy",
        "1080p AMZN WEB DL AI x265 HEVC 10bit AAC 5 1 Joy",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)",
        "(1080p BDRip x265 10bit EAC3 5.1 - Goki)[TAoE]",
        "(1080p BluRay x265 HEVC 10bit AAC 2.0 Vyndros)",
        "(1080p AMZN Webrip x265 10bit EAC3 5.1 - Goki)",
        "[1080p x265][Raw with JP Subs - Netflix] HR-MF",
        "(1080p BDRip x265 10bit EAC3 5.1 - Erie)[TAoE]",
        "(1080p BDRip x265 10bit EAC3 5.1 - Species180)",
        "1080p BluRay x265 HEVC 10bit AAC 5.1-LordVako",
        "(1080p BluRay x265 HEVC 10bit EAC3 2.0 SAMPA)",
        "1080p.BluRay.AC3.x265.HEVC.10Mbit.HUN.ViZoZoN",
        "(1080p BluRay x265 HEVC 10bit EAC3 7.1 SAMPA)",
        "(1080p BluRay x265 HEVC 10bit EAC3 5.1 SAMPA)",
        "(1080p Bluray x265 HEVC 10bit AAC 5.1 Tigole)",
        "(1080p BluRay x265 HEVC 10bit AAC 7.1 Tigole)",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 RZeroX)",
        ".1080p.BluRay.x265.HEVC.10bit.5,1ch(xxxpav69)",
        "[1080p x265 HEVC 10bit BD Dual Audio AAC 5.1]",
        "(1080p BluRay x265 HEVC 10bit AC3 1.0 SAMPA)",
        "(1080p BluRay x265 HEVC 10bit AAC 7 1 SAMPA)",
        ".1080p.Blu-Ray.10-Bit.Dual-Audio.DTS-HD.x265",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 afm72)",
        "1080p Dual Audio BDRip 10 bits DD x265-EMBER",
        ".JPN.UHD.BluRay.x265.HDR.DDP.5.1.MSubs-DTone",
        ".1080p.10bit.DSNP.WEB-DL.DDP5.1.HEVC-Vyndros",
        "2160p NF WEBRip NVENC HEVC 10bit AAC 5 1 Joy",
        "1080p NF WEBRip NVENC HEVC 10bit AAC 5 1 Joy",
        ".1080P.10Bit.Red.Web-Dl.Aac5.1.Hevc-Vyndros",
        "(1080p BluRay x265 HEVC 10bit AAC 5.1 RCVR)",
        ".1080p.AMZN.WEBRip.DDP5.1.x265-SiGMA[rartv]",
        ".1080p.NF.WEBRip.DDP5.1.Atmos.x264-NTG[TGx]",
        ".1080p.AMZN.WEBRip.DDP5.1.x264-TEPES[rarbg]",
        ".1080p.WEB-DL.x265.10bit.EAC3.2.0-Qman[UTR]",
        "1080p NF Webrip x265 10bit EAC3 5.1 - Ainz",
        ".1080p.HQ.10bit.BluRay.5.1.x265.HEVC-MZABI",
        "BR EAC3 VFF VFQ ENG 1080p x265 10Bits T0M",
        ".1080p.BluRay.x264-TheWretched [PublicHD]",
        ".BluRay.1080p.DTS.x264.Millie.Bobby.Brown",
        ".1080p.CBS.WEBRip.AAC2.0.x264-TEPES[TGx]",
        ".1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb[TGx]",
        ".1080p.DCU.WEBRip.DDP5.1.x264-NTb[rarbg]",
        ".1080P.DVDScr.X264.AC3.SHQ.Hive-CM8[TGx]",
        "(480p DVD x265 HEVC 10bit DD5.1 Vyndros)",
        "(720p)(Multiple Subtitle)-Erai-raws[TGx]",
        "(480p)(Multiple Subtitle)-Erai-raws[TGx]",
        "ITA-JAP Ac3 5.1 BDRip 1080p H264 [ArMor]",
        "[1080p BDRemux x265 DTS-HD MA 5.1] HR-MF",
        ".1080p.10bit.BluRay.5.1.x265.HEVC-MZABI",
        "(DVDRip 720x480p x265 HEVC AC3x3 2.0x3)",
        "Bluray x265 10Bit AAC 5.1 - GetSchwifty",
        ".1080p.BluRay.10bit.HEVC.6CH-MkvCage.ws",
        "[Hindi DD 640Kbps Org 5.1 - Eng DD 2.0]",
        ".1080p.H264.ita.jpn.Ac3.sub.ita-MIRCrew",
        "[ShadyCrab 1080p 8bit AAC] [Dual Audio]",
        "[1080p.x265][multisubs:eng,fre][Vostfr]",
        ".1080P.Bluray.X264.Truehd.7.1.Atmos-Fgt",
        "Bluray.1080P.Truehd.7.1.Atmos.X264-Grym",
        "AC3 5.1 ITA.ENG 1080p H265 sub ita.eng",
        ".1080p.DCU.WEB-DL.DDP5.1.H264-NTb[TGx]",
        "Blu-Ray.10-Bit.Dual-Audio.TrueHD.x265",
        ".PROPER.1080p.WEB.H264-ELiMiNATE[TGx]",
        "BR EAC3 VFF ENG 1080p x265 10Bits T0M",
        "[Hindi Dub] h.264 Dual-Audio AAC x264",
        "[1080p][BD][x265][10-bit][Dual-Audio]",
        ".1080p.10bit.BluRay.x265.HEVC.6CH-MRN",
        "VOSTFR 1080p NF WEBRip DD5.1 x264-QOQ",
        "1080p HEVC 10 Bit AC3 5.1 EN Subs EN",
        ".iNTERNAL.720p.WEB.x264-GHOSTS[eztv]",
        ".1080p.BluRay.10Bit.HEVC.EAC3-SARTRE",
        ".1080p.NF.WEBRip.DD5.1.x264-Morpheus",
        "1080p Webrip x265 AC3 5.1 Goki [SEV]",
        ".1080p.BluRay.x264-SHORTBREHD[rartv]",
        ".1080p.BluRay.x264-SONiDO [PublicHD]",
        "ITA WEBRip 1080p x265 mkv - iDN CreW",
        "[Org DD 2.0 Hindi + DD 5.1 English]",
        ".FASTSUB.VOSTFR.WEBRip.XviD.EXTREME",
        ".PROPER.1080p.BluRay.H264.AAC-RARBG",
        ".1080p.WEB-DL.DD5.1.H264-TOMMY[TGx]",
        ".1080p.BluRay.x265.HEVC.EAC3-SARTRE",
        "[DVDRip h264 720x480 10bit Vorbis]",
        ".ITA.ENG.BDrip.1080p.x264-Fratposa",
        "[1080p x265 HEVC 10bit BluRay AAC]",
        ".OAR.1080p.BluRay.x264-HD4U[rarbg]",
        ".1080p.AMZN.WEBRip.DDP2.0.x264-NTb",
        "[1080p BDRemux x265 DTS-HD MA 5.1]",
        "1080p BDRip 10 bits AAC x265-EMBER",
        "[VOSTFR BD x264 10bits 1080p FLAC]",
        ".1080p.WEB.H264-ANTAGONiST[rarbg]",
        ".1080p.WEB-DL.DD5.1.H264-BTN[TGx]",
        "(1080p BluRay x265 10bit Tigole)",
        "BDRip 1080p Ita Eng x265 - NAHOM",
        "[BD 1920x1036 HEVC 10bit OPUSx2]",
        "(Dual Audio_10bit_BD1080p_x265)",
        "(Dual Audio 10bit BD1080p x265)",
        ".1080p.BluRay.x264-REGRET[EtHD]",
        ".DVDRip.XviD-NYDIC.[UsaBit.com]",
        "10 bit 1080p HEVC BDRip [MOVIE]",
        "(1080P Atvp Web-Dl X265 T3nzin)",
        ".1080p.BluRay.AC35.1.x265-GREP",
        ".1080p.BrRip.6CH.x265.HEVC-PSA",
        "(Dual Audio_10bit_BD720p_x265)",
        "[BD 1920x1080 x265 10Bit Opus]",
        ".iNTERNAL.720p.WEB.x264-GHOSTS",
        ".1080p.HDTV.x264-FaiLED[rarbg]",
        "BDRip 1080p x264 AAC - KiNGDOM",
        "720p BluRay x264 300MB Pahe.in",
        "(BD 1920x1080 x265-10Bit Flac)",
        "[JesuSub] vostfr 720p x265 AAC",
        "[BD 1920x1080 HEVC 10bit OPUS]",
        "[eng subbed]{Neroextreme}_NTRG",
        "1080p NF WEBRip DD5.1 x264-QOQ",
        "FRENCH WEBRip NF x264-LiBERTAD",
        ".iNTERNAL.480p.x264-mSD[eztv]",
        ".WS.1080p.BluRay.x264.DTS-FGT",
        "[1080P_x265(10bit)-FLAC][ALL]",
        "MULTI 1080p WEBRip x264-ACOOL",
        "(1080p x265 HEVC AAC 5.1 Joy)",
        "(2160p x265 HEVC AAC 5.1 Joy)",
        ".720p.HDTV.HEVC.x265-MeGusta",
        "1080p.WEBRip.x264 - [YTS.AM]",
        ".x264.BDRip.(720p)-MediaClub",
        ".1080p.BluRay.H264.AAC-RARBG",
        "(BD 1080P x265 Ma10p FLACx3)",
        "1080p BluRay DUAL AUDIO x264",
        "VOSTFR WEBRip XviD AC3-ACOOL",
        "(1080p BluRay x265 Silence)",
        "[BDRip 1920x1080 x264 FLAC]",
        ".1080p.WEBRip.x264-ParovozN",
        ".1080p.BDRip.10bit.x265.AC3",
        ".x264.BDRip.1080p-MediaClub",
        "720p HDTV 2CH x265 HEVC-PSA",
        ".1080p.WEBRip.DD5.1.x264-CM",
        ".1080p.WEBRip.x264-XLF[TGx]",
        ".1080p.WEB.H264-METCON[TGx]",
        "(BD 1080p x265 10-Bit Opus)",
        "[Web-Rip 1080p x265 10 bit]",
        "(BD 1920x1080 x264+ FLACx2)",
        "ITA AC3 WEBRip H264 - L@Z59",
        "[Raw with JP Subs -Netflix]",
        "(DVDRip 1024x576 x265 FLAC)",
        "720p BluRay x264-W4F [RiCK]",
        ".1080P.Bluray.X264-Amiable",
        "[DVDRip 1280x720 h264 ac3]",
        ".1080p.BluRay.x264.AC3-DDL",
        "(DVDRip Hi10 768x576 x265)",
        "(WEBDL) 1080p x265 Ukr DVO",
        "[BD 1080p AAC HEVC 10bit]",
        "(Dual Audio_10bit_BD720p)",
        ".720p.WEB.x265-MiNX[eztv]",
        "(DVDRip 768x576 x265 AC3)",
        "(1080p x265 10bit Tigole)",
        "FRENCH WEBRip NF XviD-GZR",
        "(1080p WEB-DL x265 Panda)",
        "(1080p WEB-DL x265 RCVR)",
        "(1080p BluRay x265 RCVR)",
        ".720p.WEB.h264-TBS[eztv]",
        ".1080p.BluRay.x265-RARBG",
        "720p.HDTV.x265-MiNX[TGx]",
        ".1080p.WEBRip.x264-RARBG",
        "[FuniDub 1080p x265 AAC]",
        "(AT-X 1280x720 x264 AAC)",
        "(BD 1280x720 x264 AACx2)",
        "(BS11 1280x720 x264 AAC)",
        "(CX 1920x1080 x264+ AAC)",
        "1080p WEBRip x264-STRiFE",
        "720p WEBRip XviD AC3-FGT",
        ".hdr.2160p.web.h265-ggez",
        "[Dual Audio 10bit 720p]",
        ".iNTERNAL.480p.x264-mSD",
        ".Bluray.TrueHD-7.1-Grym",
        "1080p 10 bit x264- Obey",
        "(TBS 1280x720 x264 AAC)",
        "BD 1080p 8bit [rich_jc]",
        "1080p.x264.AAC ENG Subs",
        "[BDRip 1036p x264 FLAC]",
        "(1080p BluRay x265 ImE)",
        "(1080p WEB-DL x265 ImE)",
        "[Web 1080p HEVC Multi]",
        "(BD 1080p Hi10 FLACx2)",
        "720p BluRay x264 [i_c]",
        "1080p.BluRay.x264-HD4U",
        "(CX 1280x720 x264 AAC)",
        "(MX 1280x720 x264 AAC)",
        "1920x1080 Blu ray FLAC",
        "[1080p x265 10bit Joy]",
        "(1080p x265 10bit Joy)",
        "(1080p AMZN x265 10bit",
        "[2160p x265 10bit Joy]",
        "(2160p x265 10bit Joy)",
        "(2160p AMZN x265 10bit",
        ".Truehd.7.1.Atmos-Fgt",
        "(1920x1080 x265 flac)",
        "[UNCENSORED BD 1080p]",
        ".WEBRip.1080p.DUB+AVO",
        ".BluRay.x264.AC3-ETRG",
        ".HDTV.h264-SFM[rartv]",
        "_(10bit_BD1080p_x265)",
        "(480p TVRip x265 ImE)",
        "[1080p BD][HEVC FLAC]",
        "(1080p Web 1080p Joy)",
        "[Nep_Blanc]MULTI VFF",
        ".BDRip.1080p.Rus.Eng",
        "[ www.Torrent9.uno ]",
        ".HDTV.x264-SVA[ettv]",
        "(10bit_BD1080p_x265)",
        "[Multiple Subtitle] ",
        "720p DUAL AUDIO x264",
        "1080P HEVC 8Bit X265",
        "[1080p AI x265 10bit",
        "(1080p x265 q22 Joy)",
        "(1080p BD x265 10bit",
        "[2160p AI x265 10bit",
        "(2160p x265 q22 Joy)",
        "(2160p BD x265 10bit",
        "(Bd 1080P Hi10 Flac)",
        "(Us Bd Remux, 1080P)",
        "(Multiple Subtitle)",
        "[BluRay 1080p HEVC]",
        "(BD1080p AC3 10bit)",
        "[Kōritsu_bonkai77]",
        "(10bit_BD720p_x265)",
        "[BD 1080p HEVC AAC]",
        "BDRip.1080p.selezen",
        ".720p.WEB.x265-MiNX",
        ".WEB.h264-TBS[ettv]",
        "[WEBRip 1080p HEVC]",
        "[multisubs:eng,fre]",
        "WEBRip XviD AC3-FGT",
        ".Hdr.2160P.Web.H265",
        "[Kōritsu_bonkai77]",
        "[Eng-Subs] - Judas",
        "10bit_BD720p_x265)",
        ".DVDRip.XviD-NYDIC",
        ".720p.x265-MeGusta",
        "Mp4 x264 AC3 1080p",
        ".WEBRip.x264-ION10",
        "Ita Eng x265-NAHOM",
        "1080p HEVC AC3 5.1",
        "HDR.2160p.WEB.H265",
        "[BD 2160p 4K UHD]",
        "[HEVC x265 10bit]",
        "8-bit FLAC 16-bit",
        "[Complete Subbed]",
        "1080p.WEBRip.x264",
        "Dual.Audio.Bluray",
        "[1080p x265 10bit",
        "(1080p x265 10bit",
        "[2160p x265 10bit",
        ".1080p.x265-ZMNT",
        "[JacobSwaggedUp]",
        "(BD Batch + OVA)",
        "[1080p-AC3-FLAC]",
        "(Exiled-Destiny)",
        "[Exiled-Destiny]",
        "[Coalgirls-subs]",
        "Sp33dy94-MIRCrew",
        "[HEVC x265 8bit]",
        "x265 10bits PTBR",
        "(1080p x265 Joy)",
        "[HEVC-reencode]",
        "WEB-DLRip.1080p",
        "[LowPower-Raws]",
        "[v2][AnimeKayo]",
        "[Beatrice-Raws]",
        "[SEKAI PROJECT]",
        "WEBRip x264-FGT",
        "[1080p x265 q22",
        "(1080p x265 q23",
        "(1080p x265 q22",
        "(1080p x265 q21",
        "(1080p x265 q20",
        "(1080p x265 q19",
        "(1080p x265 q18",
        "[2160p x265 q22",
        "(2160p x265 q23",
        "(2160p x265 q22",
        "(2160p x265 q21",
        "(2160p x265 q20",
        "(2160p x265 q19",
        "(2160p x265 q18",
        ".1080P.Tvshows",
        "1080p x265 Joy",
        "(Diamond Luxe)",
        "1080p.WEB.x264",
        "[HorribleSubs]",
        "[BlurayDesuYo]",
        "[BD 1080p AAC]",
        "[Shinkiro-raw]",
        ".720p.WEB.x265",
        ".720p.HDTV.TNT",
        "[WEBRip 1080p]",
        "TVRip x265 ImE",
        "[1080p AI x265",
        "[2160p AI x265",
        "Theatrical Cut",
        "[AkihitoSubs]",
        "[anime4life.]",
        "(BD 1280x720)",
        "[Multi-Audio]",
        "[Ma10p_1080p]",
        ".720p.HDTVRip",
        "[Halfwitsubs]",
        "[BDRip 1080p]",
        "[H.265 10bit]",
        "[Delivroozzi]",
        "Directors Cut",
        "[Multi-Subs]",
        "[kokus-rips]",
        "[1080p HEVC]",
        "[AnimeCreed]",
        "[DragsterPS]",
        "[VCB-Studio]",
        "[Ma10p_720p]",
        "[Dual-Audio]",
        "[GrimRipper]",
        "FLACx2 2.0x2",
        "(Dual Audio)",
        "[hshare.net]",
        "Vorbis[IMAX]",
        "WEB-DL.1080p",
        "[RiP By MaX]",
        "[UsaBit.com]",
        "[Anime Time]",
        "[SubsPlease]",
        "[Erai-raws] ",
        "[UNCENSORED]",
        "[mal lu zen]",
        "[1080p x265]",
        "[MiniFreeza]",
        "[eng subbed]",
        "[1080p.x265]",
        "[HDRip][MVO]",
        "HEVC AC3 5.1",
        "MVL.BDRemux",
        "PSArips.com",
        "(Criterion)",
        "English-Dub",
        "[HEVC-x265]",
        "[Nep_Blanc]",
        "[x265_HEVC]",
        "[ZetaRebel]",
        "[Lazy Lily]",
        "[Mezashite]",
        "-Judas[TGx]",
        "[Kaerizaki]",
        "SubsPlease]",
        "[Ohys-Raws]",
        "[Hentai 2D]",
        "FullHD x265",
        "[Noob-Subs]",
        "[SAIO Raws]",
        "AC3x2 2.0x2",
        "Atmos-MIXED",
        "PETFRiFiED",
        "[x264][BD]",
        "[BD 1080p]",
        "Dual Audio",
        "Dual_Audio",
        "[Cerberus]",
        "[Shisukon]",
        "[Tsundere]",
        "(DVD_480p)",
        "[ENG.SUBS]",
        " 91V55V 93",
        "(xxxpav69)",
        "[PublicHD]",
        "(BD Batch)",
        "(Batch) v2",
        "[Marshall]",
        "Ohys-Raws]",
        "HDRip] Dub",
        "Open Matte",
        "Hindi Dub]",
        "[Hakobune]",
        "[Eng-Subs]",
        "[japanese]",
        "[BD 1036p]",
        "[bonkai77]",
        "Theatrical",
        "x265-GREP",
        "Web 1080p",
        "Erai-raws",
        "D0ct0rLew",
        "(JPN ENG)",
        "[GSK_kun]",
        "[Kametsu]",
        "[Aeenald]",
        "[Chimera]",
        "[neoHEVC]",
        "[Reaktor]",
        "[FFFmpeg]",
        "WEB-720PX",
        "[pkanime]",
        "[960x720]",
        "[EROBEAT]",
        "[BDremux]",
        "MediaClub",
        "[Taedium]",
        "Mp4 1080p",
        "[Moozzi2]",
        "[AnimeRG]",
        "[FY-Raws]",
        "[DavRips]",
        "WEB-DLRip",
        "[AVC AAC]",
        "[Skytree]",
        "[JesuSub]",
        "[Maximus]",
        "[Blu Ray]",
        "[rich_jc]",
        "[AniFilm]",
        "[RUS+JAP]",
        "Directors",
        "X264-Grym",
        "LordVako",
        "HEVC-PSA",
        "WEB.x264",
        "[Subbed]",
        "WEB.h264",
        "[UTR-HD]",
        "YURASUKA",
        "[AAC]ENG",
        "[KgOlve]",
        "[Ranger]",
        "1024x576",
        "720x480p",
        "[sxales]",
        "[YTS.LT]",
        "Fratposa",
        "ParovozN",
        "[pseudo]",
        "[YTS.AG]",
        "[YTS.AM]",
        "[infanf]",
        "(Weekly)",
        "[WEB-DL]",
        "iDN CreW",
        "Eng-Subs",
        "[YTS AM]",
        "[Nemuri]",
        "Vyndros",
        "BD1080p",
        "[ZRIPZ]",
        "[10Bit]",
        "[1080p]",
        "[Pixel]",
        "FLAC2.0",
        "[Judas]",
        "BDRemux",
        "[wat15]",
        "720x480",
        "Blu-Ray",
        "[ShowY]",
        "[EMBER]",
        "[UNCEN]",
        "[UNCUT]",
        "DUB+AVO",
        "MkvCage",
        "[rarbg]",
        "(Batch)",
        "[kmplx]",
        "UNRATED",
        "ITA-JAP",
        "[ArMor]",
        "[Batch]",
        "[CuaP] ",
        "[CRRIP]",
        "(WEBDL)",
        "Blu ray",
        "[CHiP] ",
        "[MOVIE]",
        "[h.265]",
        "(Pilot)",
        "TombDoc",
        "Amiable",
        "seleZen"
        "E-OPUS",
        "[Cleo]",
        "[Opus]",
        "[x265]",
        "[HEVC]",
        "WEBrip",
        "BD720p",
        "Subbed",
        "Dubbed",
        "[720p]",
        "10-Bit",
        "BluRay",
        "FLACx2",
        "10Bits",
        "WEB-DL",
        "[Edge]",
        "DVDRip",
        "[WBDP]",
        "16-bit",
        "(Hi10)",
        "[Prof]",
        "DTS-HD",
        "[Dual]",
        "[Subs]",
        "TrueHD",
        "( HT )",
        "[~AA~]",
        "[EtHD]",
        "[eztv]",
        "FaiLED",
        "[480p]",
        "EmKayy",
        "-MEECH",
        "[TAoE]",
        "-RARBG",
        "VOSTFR",
        "[Baha]",
        "(540p)",
        "[LWND]",
        "[35mm]",
        "-ACOOL",
        "[YIFY]",
        "[RiCK]",
        "DDP5.1",
        "Atmos",
        "2160p",
        "HR-RG",
        "HR-GZ",
        "HR-DR",
        "HR-SW",
        "[AAC]",
        "Judas",
        "[TGx]",
        "[SEV]",
        "1080p",
        "BDRip",
        "10Bit",
        "[ANE]",
        "[CBM]",
        "[HQR]",
        "[5.1]",
        "8-bit",
        "BrRip",
        "[FFF]",
        "[cen]",
        "[scy]",
        "[DVD]",
        "[UTR]",
        "[i_c]",
        "RARBG",
        ".DVD9",
        "HR-SR",
        "[ASW]",
        "HDRip",
        "[NEW]",
        "[CHT]",
        "[MP4]",
        "h.264",
        "HR-MF",
        "[zza]",
        "[HDR]",
        "(HDR)",
        "[YnK]",
        "1036p",
        "[YTS]",
        "[5 1]",
        "[RAW]",
        "h.265",
        "TVRip",
        "[Npz]",
        ".hdr.",
        " hdr ",
        "KOGi",
        "BDMV",
        "HDR.",
        ".HDR",
        "glhf",
        "ggwp",
        "ggez",
        "ZMNT",
        "720p",
        " 4k ",
        " UHD",
        "480p",
        "x264",
        "[HR]",
        "h264",
        "h265",
        "DSNP",
        "x265",
        "Opus",
        "[DB]",
        "Hi10",
        "ETTV",
        "[KH]",
        "HR-J",
        "iAHD",
        "[HD]",
        "~AA~",
        "V55V",
        "DVD9",
        " DC ",
        "CBM]",
        "EAC3",
        "T0M",
        "DVD",
        "JPN",
        "Scy",
        "vxt",
        "[]",
        "()",
        "{}",
        ]

    # List duplication checker :)
    #checkForDups(removeStrings)

    removeStringsSorted = (sorted(removeStrings, key=len, reverse=True))

    #for item in removeStringsSorted:
    #    print(item)

    #breakpoint()

    outputFilename = filename[:-4]  # Remove last 4 characters = .mkv or .mp4 etc

    for item in removeStringsSorted:
        #print("\"" + item + "\",")
        # covert strings to lowercase, why? because re.sub and []() don't work together
        outputFilenameLower = outputFilename.lower()
        itemLower = item.lower()

        if not outputFilenameLower.find(itemLower)+len(itemLower) == len(itemLower) - 1:

            # Beautiful, we don't work on the actual filename, so original uppercase and lowercase is unchanged
            # only subtracting the positions
            outputFilename = outputFilename[:outputFilenameLower.find(itemLower)] + outputFilename[outputFilenameLower.find(itemLower) + len(item):]

    outputFilename = re.sub("FS[0-9][0-9] Joy\)", "", outputFilename, flags=re.I)           # Take this joy
    outputFilename = re.sub("FS[0-9][0-9] Joy]", "", outputFilename, flags=re.I)           # And your dumb filenames
    outputFilename = re.sub("FS[0-9][0-9][0-9] Joy\)", "", outputFilename, flags=re.I)      # Yes i did write a regex
    outputFilename = re.sub("FS[0-9][0-9][0-9] Joy]", "", outputFilename, flags=re.I)      #
    outputFilename = re.sub("S[0-9][0-9] Joy\)", "", outputFilename, flags=re.I)            # for one person
    outputFilename = re.sub("S[0-9][0-9] Joy]", "", outputFilename, flags=re.I)            #

    outputFilename = re.sub("\[[^\[][^\[][^\[][^\[][^\[][^\[][^\[][^\[]]", "", outputFilename, flags=re.I)  # remove e.g.[ABC12345]
    outputFilename = re.sub("\([^\[][^\[][^\[][^\[][^\[][^\[][^\[][^\[]\)", "", outputFilename, flags=re.I)  # remove e.g.(ABC12345)

    #outputFilename = re.sub("\.$", "", outputFilename)
    #print(re.search("\.$", outputFilename))

    outputFilename = re.sub("-[0-9][0-9]$", "", outputFilename, flags=re.I)  # Handbrake puts -X or -XX at end of files
    outputFilename = re.sub("-[0-9]$", "", outputFilename, flags=re.I)

    if not re.search("S[0-9][0-9]E[0-9][0-9].[0-9] ", outputFilename):  # If S01E01.5(space), then skip removing dots (Some use the .5 for a second part of an episode)
        if outputFilename.count(".") >= 2 and re.search("\.$", outputFilename) is None:  # if theres 2 or more dots
            outputFilename = outputFilename.replace(".", " ")  # _ is usually a stand in for a space
    outputFilename = re.sub("\.$", "", outputFilename)
    outputFilename = outputFilename.replace("_", " ")  # _ is usually a stand in for a space

    outputFilename = re.sub("\s\s+", " ", outputFilename)  # Make 2 or more continuous spaces into one

    outputFilename = outputFilename.replace("( )", "")  # Remove empty brackets
    outputFilename = outputFilename.replace("[ ]", "")  # Remove empty brackets



    import datetime
    now = datetime.datetime.now()

    currentDecade = str(now.year)[2]
    currentYear = str(now.year)[3]

    # Remove numbers 1920 to current year

    outputFilename = re.sub(r"\s20[0-" + currentDecade + "][0-" + currentYear + "]", "", outputFilename)
    outputFilename = re.sub(r"\s20[0-1][0-9]", "", outputFilename)
    outputFilename = re.sub(r"\s19[2-9][0-9]", "", outputFilename)

    outputFilename = re.sub("\([0-9][0-9][0-9][0-9]\)", "", outputFilename)  # Remove Years eg. (1994) NOTE: Don't remove years with spaces on both sides
    outputFilename = re.sub("\[[0-9][0-9][0-9][0-9]]", "", outputFilename)  # [1994]


    outputFilename = re.sub(r"ep ([0-9][0-9])", r"E\1", outputFilename, flags=re.I)  # ep 13 to E13
    outputFilename = re.sub(r"ep ([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep 3 to E03
    outputFilename = re.sub(r"Episode ([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep 3 to E03

    outputFilename = re.sub(r"ep([0-9][0-9])", r"E\1", outputFilename, flags=re.I)  # ep03 to E03
    outputFilename = re.sub(r"ep([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep3 to E03 Haven't seen one with this case, but il code it in anyway

    outputFilename = re.sub("- ([0-9][0-9][0-9])$", r" E\1 ", outputFilename)  # Replace "- 001" with E001, why would any have so may episodes, IDK
    outputFilename = re.sub("-([0-9][0-9])$", r" E\1 ", outputFilename)  # Replace -01 If at end of file name
    outputFilename = re.sub("\[([0-9][0-9])]", r" E\1 ", outputFilename)  # Replace [01] with E01

    outputFilename = re.sub("e([0-9][0-9])", r"E\1 ", outputFilename)  #S01e01 > S01E01

    outputFilename = re.sub("([0-9][0-9])x([0-9][0-9])", r" S\1E\2 ", outputFilename, flags=re.I)  # 11x01 to S11E01
    outputFilename = re.sub("([0-9])x([0-9][0-9])", r" S0\1E\2 ", outputFilename, flags=re.I)  # 1x01 to S01E01

    outputFilename = re.sub("(S[0-9][0-9]E[0-9][0-9]) -", r"\1", outputFilename, flags=re.I)  # Removes space + Hyphen (S11E01 -)
    outputFilename = re.sub(" - (S[0-9][0-9]E[0-9][0-9])", r" \1", outputFilename, flags=re.I)  # Removes space + Hyphen + space ( - S11E01) to ( S11E01)

    outputFilename = outputFilename.replace(" -", " ")
    outputFilename = outputFilename.replace("- ", " ")
    outputFilename = re.sub("(-$)", "", outputFilename, flags=re.I)  # test-.mkv to test.mkv

    outputFilename = re.sub("(\([0-9]\))", "", outputFilename, flags=re.I)  # remove (1)
    outputFilename = re.sub("(-[0-9]$)", "", outputFilename, flags=re.I)  # test-4.mkv to test.mkv
    outputFilename = re.sub("(-[0-9][0-9]$)", "", outputFilename, flags=re.I)  # test-99.mkv to test.mkv

    # print(outputFilename)

    outputFilename = re.sub("\s\s+", " ", outputFilename)  # Make 2 or more continuous spaces into one, yes we do this twice
    outputFilename = outputFilename.strip()  # Remove leading and trailing whitespaces
    outputFilename = re.sub("\s([0-9][0-9])\s", r" E\1 ", outputFilename)  # Replace (space + 02 + space) If there are double digits left at is stage this its probably an Ep number

    if re.search("\s[0-9]{2}$", outputFilename):
        if previousOutputFilename[:-2] == (re.sub("\s([0-9][0-9])$", r" E\1 ", outputFilename).strip())[:-2]:  # Optimize if everything but the last two characters are the same
            outputFilename = re.sub("\s([0-9][0-9])$", r" E\1 ", outputFilename)
        else:
            from function_getRuntime import getRuntime
            if getRuntime(currentOS, filenameAndDirectory, filename) < 4001:  # if over 1.1 hours long, its probably not an episode
                outputFilename = re.sub("\s([0-9][0-9])$", r" E\1 ", outputFilename)  # If there are two digits at the end of the filename, then there probably an episode number, only on .mkv files

    outputFilename = outputFilename.strip()  # Remove leading and trailing whitespaces
    outputFilename += ".mkv"  # Add extension

    #print(outputFilename)

    return outputFilename
