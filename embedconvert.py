import discord
import json
import sqlite3

embeds = []

embed = discord.Embed(title="FIST", url='http://wiki.erepublik.com/index.php/Formidable_International_Security_Treaty',
                      description="FIST (Formidable International Security Treaty) was an Alliance focused in Asia. It's six members all signed the Charter of the PEACE Global Community when it was created, dissolving FIST.",
                      color=0xffff00)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/c/cf/Flag-FIST.jpg')
embed.add_field(name="Formation", value="Day 191", inline=False)
embed.add_field(name="Disbanded", value="Day 280", inline=False)
embed.add_field(name="All time members", value="6", inline=True)
embed.add_field(name="Founders",
                value=":flag_id: Indonesia - :flag_ir: Iran - :flag_jp: Japan - :flag_pk: Pakistan - :flag_tr: Turkey",
                inline=True)
embed.add_field(name="Other member", value=":flag_gr: Greece", inline=True)

embeds.append(embed)

embed = discord.Embed(title="Northern Alliance", url='http://wiki.erepublik.com/index.php/Northern_Alliance',
                      description="The NA was an Alliance of countries in Northern Europe and Scandinavia. Other countries such as Romania and the United States also joined. Most of the NA's members eventually joined ATLANTIS when it was formed.",
                      color=0xffff00)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/0/07/Undefined-flag.gif')
embed.add_field(name="Formation", value="Day 56", inline=False)
embed.add_field(name="Disbanded", value="Day 100", inline=False)
embed.add_field(name="All time members", value="6", inline=True)
embed.add_field(name="Founders",
                value=":flag_ei: Ireland - :flag_no: Norway - :flag_ro: Romania - :flag_se: Sweden - :flag_gb: United Kingdom - :flag_us: USA",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="Mediterranean Alliance", url='http://wiki.erepublik.com/index.php/Mediterranean_Alliance',
                      description="The MA was an alliance comprising of eight countries in Southern Europe and North America. The alliance was founded by Spain to consist of Nations bordering the Mediterranean Sea, later other countries such as Austria, the Netherlands and Canada joined. Eventually the MA collapsed due to rifts between pro-FIST nations, who later formed PEACE GC, and pro-NA nations who united to form ATLANTIS.",
                      color=0x000000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/0/07/Undefined-flag.gif')
embed.add_field(name="Formation", value="Unknown", inline=False)
embed.add_field(name="Disbanded", value="Day 224", inline=False)
embed.add_field(name="All time members", value="8", inline=False)
embed.add_field(name="Founders", value=":flag_es: Spain", inline=False)
embed.add_field(name="Other members",
                value=":flag_at: Austria - :flag_ca: Canada - :flag_fr: France - :flag_hu: Hungary - :flag_it: Italy - :flag_nl: Netherlands - :flag_pt: Portugal",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="Byzantine Empire", url='http://wiki.erepublik.com/index.php/Byzantine_Empire',
                      description="The Byzantine Empire was an Eastern European Alliance comprised of two countries, Greece and Turkey. The alliance lasted for less than a month and ended with the first death of Phaedrus Lidox. As both countries signed the Formidable International Security Treaty, it is sometimes considered a sub-alliance of FIST.",
                      color=0xff0000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/2/29/Flag-New_Byzantine_Empire.jpg')
embed.add_field(name="Formation", value="Day 257", inline=False)
embed.add_field(name="Disbanded", value="Day 276", inline=False)
embed.add_field(name="All time members", value="2", inline=False)
embed.add_field(name="Founders", value=":flag_gr: Greece - :flag_tr: Turkey", inline=False)

embeds.append(embed)

embed = discord.Embed(title="PANAM", url='http://wiki.erepublik.com/index.php/Pan_American_Alliance',
                      description="PANAM (Pan American Alliance) was an Alliance consisting of five of the six eRepublik countries in North and South America. The Alliance eventually formed the basis of ATLANTIS, even though only 2 of the five countries remained in it.",
                      color=0x000000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/0/07/Undefined-flag.gif')
embed.add_field(name="Formation", value="Day 88", inline=False)
embed.add_field(name="Disbanded", value="Day 270", inline=False)
embed.add_field(name="All time members", value="5", inline=False)
embed.add_field(name="Founders",
                value=":flag_ar: Argentina - :flag_br:  Brazil - :flag_mx: Mexico - :flag_ve: Venezuela - :flag_us: USA",
                inline=False)

embeds.append(embed)

embed = discord.Embed(title="ATLANTIS", url='http://wiki.erepublik.com/index.php/ATLANTIS',
                      description="ATLANTIS (Atlantic Treaty of Latin, American, and Nordic Territories for International Security) was a large military alliance consisting of several member nations. For a long time it was one of two active alliances in eRepublik (the second being PEACE) and, of the two, it had the larger military. ATLANTIS collapsed after infighting following the loss of World War II and the Third Sweden-Germany War between two ATLANTIS members.",
                      color=0x000080)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/e/e3/Flag-ATLANTIS.jpg')
embed.add_field(name="Formation", value="Day 276", inline=False)
embed.add_field(name="Disbanded", value="Day 548", inline=False)
embed.add_field(name="All time members", value="15", inline=False)
embed.add_field(name="Founders",
                value=":flag_no: Norway - :flag_ro: Romania - :flag_se: Sweden - :flag_gb: United Kingdom - :flag_us: USA - :flag_es: Spain - :flag_ar: Argentina",
                inline=False)
embed.add_field(name="Other members",
                value=":flag_ba: Bosnia and Herzegovina - :flag_ca: Canada - :flag_hr: Croatia - :flag_fi: Finland - :flag_de: Germany - :flag_gr: Greece - :flag_il: Israël - :flag_pl: Poland",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="PEACE GC", url='http://wiki.erepublik.com/index.php/PEACE',
                      description="The PEACE (People of Earth Associated under Common Excellence) Global Community was a worldwide military alliance consisting of all former FIST member nations as well as many former Mediterranean Alliance members. It was the largest and oldest continuously existing alliance.",
                      color=0x0080c0)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/b/b7/Seal-PEACE-GC-White.jpg')
embed.add_field(name="Formation", value="Day 280", inline=False)
embed.add_field(name="Disbanded", value="Day 730", inline=False)
embed.add_field(name="All time members", value=" 34", inline=False)
embed.add_field(name="Founders",
                value=":flag_pk: Pakistan - :flag_gr: Greece - :flag_tr: Turkey - :flag_bg: Bulgaria - :flag_hu: HUngary - :flag_at: Austria - :flag_it: Italy - :flag_fr: France - :flag_ir: Iran - :flag_id: Indonesia - :flag_jp: Japan - :flag_pt: Portugal - :flag_ve: Venezuela - :flag_br: Brazil - :flag_nl: Netherlands",
                inline=False)
embed.add_field(name="Other members",
                value=":flag_ar: Argentina - :flag_bo: Bolivia - :flag_cl: Chile - :flag_co: Colombie - :flag_ee: Estonia - :flag_de: Germany - :flag_lv: Latvia - :flag_lt: Lithuania - :flag_mx: Mexico - :flag_py: Paraguay - :flag_ph: Philippines - :flag_ru: Russia - :flag_rs: Serbia - :flag_si: Slovenia - :flag_th: Thailand - :flag_ua: Ukraine - :flag_gb: United Kingdom - :flag_be: Belgium - :flag_uy: Uruguay",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="ALA", url='http://wiki.erepublik.com/index.php/ALA',
                      description="ALA (Alianza Latino Americana - Spanish: Latino-American Alliance) was a defensive alliance of Latin American countries. It was based in the Real Life European Union.",
                      color=0xf09917)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/7/75/Flag-AHA.jpg')
embed.add_field(name="Formation", value="481", inline=False)
embed.add_field(name="Disbanded", value="858", inline=False)
embed.add_field(name="All time members", value="10", inline=True)
embed.add_field(name="Founders",
                value=":flag_ar: Argentina - :flag_cl: Chile - :flag_mx: Mexico - :flag_ve: Venezuela - :flag_br: Brazil",
                inline=True)
embed.add_field(name="Other members",
                value=":flag_co: Colombia - :flag_bo: Bolivia - :flag_py: Paraguay - :flag_pe: Pery - :flag_uy: Uruguay",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="Sol", url='http://wiki.erepublik.com/index.php/Sol',
                      description="Sol was a global alliance having most of its members located in the Asia-Pacific region. It was officially a neutral defensive alliance.",
                      color=0xf52f12)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/7/71/Flag-SOL.png')
embed.add_field(name="Formation", value="596", inline=False)
embed.add_field(name="Disbanded", value="938", inline=False)
embed.add_field(name="All time members", value="11", inline=True)
embed.add_field(name="Founders",
                value=":flag_au: Australia - :flag_cn: China - :flag_jp: Japan - :flag_my: Malaysia - :flag_pk: Pakistan - :flag_ph: Philippines - :flag_sg: Singapore",
                inline=True)
embed.add_field(name="Other members",
                value=":flag_bo: Bolivia - :flag_il: Israël - :flag_za: South Africa - :flag_th: Thailand", inline=True)

embeds.append(embed)

embed = discord.Embed(title="Fortis", url='http://wiki.erepublik.com/index.php/Fortis',
                      description="Fortis was meant to be the second successor alliance of ATLANTIS. It consisted of United States of America and Canada. Originally the United Kingdom, Ireland and Spain were going to be members, but problems when the UK dropped out of negotiations and defected to PEACE. This forced Ireland to drop out as well, and no one ever signed the treaty. Spain joined EDEN, and the USA and Canada formed the Brolliance, and later joined EDEN. Ireland remained neutral. Despite having never existed, people occasionally refer to the USA and Canada as Fortis.",
                      color=0x838682)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/3/33/Flag-Fortis.jpg')
embed.add_field(name="Formation", value="595", inline=False)
embed.add_field(name="Disbanded", value="711", inline=False)
embed.add_field(name="All time members", value="2", inline=False)
embed.add_field(name="Founders", value=":flag_ca: Canada - :flag_us: USA", inline=True)

embeds.append(embed)

embed = discord.Embed(title="Brolliance", url='http://wiki.erepublik.com/index.php/Brolliance',
                      description="Brolliance (Brother-Alliance), was a successor to the Fortis alliance. It was formed originally between USA and Canada during the PEACE invasion of North America. It had expanded to include Australia, Ireland and Japan.",
                      color=0x838682)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/2/25/Flag-Brolliance.jpg')
embed.add_field(name="Formation", value="711", inline=False)
embed.add_field(name="Disbanded", value="1121", inline=False)
embed.add_field(name="All time members", value="5", inline=False)
embed.add_field(name="Founders", value=":flag_ca: Canada - :flag_us: USA", inline=True)
embed.add_field(name="Other members", value=":flag_au: Australia - :flag_ie: Ireland - :flag_jp: Japan", inline=True)

embeds.append(embed)

embed = discord.Embed(title="Entente", url='http://wiki.erepublik.com/index.php/Entente',
                      description="The Entente was an alliance founded by France, Italy and Ukraine. It was founded during Spain's invasion of France.",
                      color=0xa4a400)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/e/ef/Flag-Entente.png')
embed.add_field(name="Formation", value="776", inline=False)
embed.add_field(name="Disbanded", value="1004", inline=False)
embed.add_field(name="All time members", value="7", inline=False)
embed.add_field(name="Founders", value=":flag_fr: France - :flag_it: Italy - :flag_ua: Ukraine", inline=True)
embed.add_field(name="Other members",
                value=":flag_be: Belgium - :flag_mx: Mexico - :flag_py: Paraguay - :flag_ve: Venezuela", inline=True)

embeds.append(embed)

embed = discord.Embed(title="Phoenix", url='http://wiki.erepublik.com/index.php/Phoenix',
                      description="Phoenix was a militaristic offensive alliance that consists of ex-PEACE member nations. It was created after the majority of PEACE members resigned from that alliance.",
                      color=0xc60000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/2/22/Flag-Phoenix.png')
embed.add_field(name="Formation", value="745", inline=False)
embed.add_field(name="Disbanded", value="1183", inline=False)
embed.add_field(name="All time members", value="21", inline=False)
embed.add_field(name="Founders",
                value=":flag_br: Brazil - :flag_ee: Estonia - :flag_de: Germany - :flag_hu: Hungary - :flag_id: Indonesia - :flag_ir: Iran - :flag_lv: Latvia - :flag_lt: Lithuania - :flag_nl: Netherlands - :flag_pt: Portugal - :flag_ru: Russia - :flag_rs: Serbia - :flag_si: Slovenia - :flag_tr: Turkey - :flag_gb: United Kingdom",
                inline=True)
embed.add_field(name="Other members",
                value=":flag_bg: Bulgaria - :flag_ar: Argentina - :flag_fr: France - :flag_ua: Ukraine - :flag_me: Montenegro - :flag_mk: Macedonia",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="ONE", url='http://wiki.erepublik.com/index.php/Order_of_Nations_of_eRepublik',
                      description="ONE was a military alliance having most of its members located in the Asia-Pacific region and in Europe. It was in the process of being constructed before becoming inactive and therefore defunct.",
                      color=0xffffff)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/6/66/Flag-Order_of_Nations_of_eRepublik.png')
embed.add_field(name="Formation", value="980", inline=False)
embed.add_field(name="Disbanded", value="1054", inline=False)
embed.add_field(name="All time members", value="7", inline=False)
embed.add_field(name="Founders",
                value=":flag_at: Austria - :flag_be: Belgium - :flag_cz: Czech Republic - :flag_il: Israël - :flag_my: Malaysia - :flag_sg: Singapore - :flag_th: Thailand",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="PACMAN", url='http://wiki.erepublik.com/index.php/PACMAN',
                      description="PACMAN (Pacific-Asian Compact for Mutually-Assured Neutrality ), was a successor to the Sol/ONE alliances. Though this alliance had less members.",
                      color=0xdd0207)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/5/5b/Flag-PACMAN.png')
embed.add_field(name="Formation", value="1108", inline=False)
embed.add_field(name="Disbanded", value="1158", inline=False)
embed.add_field(name="All time members", value="3", inline=False)
embed.add_field(name="Founders", value=":flag_my: Malaysia - :flag_ph: Philippines - :flag_sg: Singapore", inline=False)

embeds.append(embed)

embed = discord.Embed(title="Luna", url='http://wiki.erepublik.com/index.php/Luna',
                      description="Luna was an independent country defensive alliance [1] It's aims, according to the Luna Introduction [1] were:  To build a community; Prevent Political Take-Overs; To defend alliance members. It aimed to succeed where such alliances as ONE and Sol both failed, as \"ineffective 'neutral' alliance[s]\".",
                      color=0xdd0207)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/f/fd/Flag-Luna.png')
embed.add_field(name="Formation", value="1229", inline=False)
embed.add_field(name="Disbanded", value="1364", inline=False)
embed.add_field(name="All time members", value="7", inline=False)
embed.add_field(name="Founders",
                value=":flag_il: Israël - :flag_in: India - :flag_ph: Philippines - :flag_my: Malaysia", inline=False)
embed.add_field(name="Other members", value=":flag_ch: Switzerland - :flag_at: Austria - :flag_uy: Uruguay",
                inline=True)

embeds.append(embed)

embed = discord.Embed(title="CAS", url='http://wiki.erepublik.com/index.php/Confederation_of_Arab_States',
                      description="The Confederation of Arab States is a step towards the ultimate Union between All Arab states, its mission is to help merge and integrate the States, politically, socially, economically, and culturally. each country will remain to control its affairs, with an independent Flag, and President, and Congress.",
                      color=0x804000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/1/1c/Flag-Confederation_of_Arab_States.png')
embed.add_field(name="Formation", value="1303", inline=False)
embed.add_field(name="Disbanded", value="1411", inline=False)
embed.add_field(name="All time members", value="2", inline=False)
embed.add_field(name="Founders", value=":flag_eg: Egypt - :flag_sa: Saudi Arabia", inline=False)

embeds.append(embed)

embed = discord.Embed(title="EPIC",
                      url='http://wiki.erepublik.com/index.php/ERepublik_Partnership_of_Interdependent_Countries',
                      description="EPIC (The eRepublik Partnership of Interdepent Countries) was a military alliance consisting of 12 members formerly known as proONE.",
                      color=0x00b3b3)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/0/0c/Flag-EPIC.png')
embed.add_field(name="Formation", value="1539", inline=False)
embed.add_field(name="Disbanded", value="1669", inline=False)
embed.add_field(name="All time members", value="13", inline=False)
embed.add_field(name="Founders",
                value=":flag_mx: Mexico - :flag_me: Montenegro - :flag_nz: New Zealand - :flag_pk: Pakistan - :flag_py: Paraguay - :flag_pe: Peru - :flag_sk: South Korea - :flag_sk: Slovakia - :thinking: Thailand - :flag_ae: United Arab Emirates - :flag_ve: Venezuela",
                inline=False)
embed.add_field(name="Other members", value=":flag_at: Austria - :flag_eg: Egypt", inline=True)

embeds.append(embed)

embed = discord.Embed(title="ONE (NWO)", url='http://wiki.erepublik.com/index.php/Order_of_New_EWorld',
                      description="ONE (Order of New Eworld, formerly known as NWO) was a Alliance consisting of several European and non-European eRepublik countries.",
                      color=0x00cece)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/8/87/Flag-ONE.jpg')
embed.add_field(name="Formation", value="1183", inline=False)
embed.add_field(name="Disbanded", value="1719", inline=False)
embed.add_field(name="All time members", value="10", inline=False)
embed.add_field(name="Founders", value=":flag_hu: Hungary - :flag_pl: Poland - :flag_rs: Serbia - :flag_es: Spain",
                inline=False)
embed.add_field(name="Other members",
                value=":flag_id: Indonesia - :flag_ir: Iran - :flag_mk: Macedonia - :flag_si: Slovenia - :flag_se: Sweden - :flag_gb: United Kingdom",
                inline=False)

embeds.append(embed)

embed = discord.Embed(title="Terra", url='http://wiki.erepublik.com/index.php/Terra',
                      description="Terra was created around mid December 2010 and at the time was called PANAM. Brazil and Argentina had withdrawn their membership from the PHOENIX alliance in the previous weeks. This freed both countries up to begin discussing a possible alliance with the USA. Brazil and the USA were the first to solidify the alliance with the signing of a Mutual Protection Pact, which shortly thereafter was cemented by the joining of Argentinian, thus giving rise to the Pan-American flavor of the alliance.",
                      color=0x0000ff)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/archive/9/94/20131012010638%21Flag-Terra.png')
embed.add_field(name="Formation", value="1121", inline=False)
embed.add_field(name="Disbanded", value="1761", inline=False)
embed.add_field(name="All time members", value="13", inline=False)
embed.add_field(name="Founders", value=":flag_br: Brazil - :flag_ar: Argentina - :flag_us: USA", inline=False)
embed.add_field(name="Other members",
                value=":flag_ca: Canada - :flag_cl: Chile - :flag_co: Colombia - :flag_cy: Cyprus - :flag_fr: France - :flag_de: Germany - :flag_jp: Japan - :flag_pt: Portugal - :flag_ru: Russia - :flag_gb: United Kingdom",
                inline=False)

embeds.append(embed)

embed = discord.Embed(title="CTRL", url='http://wiki.erepublik.com/index.php/Came_To_Rock,_Literally',
                      description="CTRL (Came To Rock, Literally) was a military alliance consisting of 4 members.",
                      color=0xff8000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/d/d1/Flag-CTRL.png')
embed.add_field(name="Fomation", value="1777", inline=False)
embed.add_field(name="Disbanded", value="1807", inline=False)
embed.add_field(name="All time members", value="4", inline=False)
embed.add_field(name="Founders", value=":flag_br: Brazil - :flag_pl: Poland - :flag_es: Spain - :flag_us: USA",
                inline=False)

embeds.append(embed)

embed = discord.Embed(title="ABC", url='http://wiki.erepublik.com/index.php/Alliance_of_Baltic_Countries',
                      description="ABC (The Alliance of Baltic Countries) was a military alliance consisting of 3 members who border each other.",
                      color=0x800000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/c/c4/Flag-ABC.png')
embed.add_field(name="Fomation", value="1228", inline=False)
embed.add_field(name="Disbanded", value="1839", inline=False)
embed.add_field(name="All time members", value="3", inline=False)
embed.add_field(name="Founders", value=":flag_ee: Estonia - :flag_lt: Lithuania - :flag_lv: Latvia", inline=False)

embeds.append(embed)

embed = discord.Embed(title="GEA", url='http://wiki.erepublik.com/index.php/Garden_of_EDEN_Alliance',
                      description="GEA (Garden of Eden Alliance) was a military alliance popularly accepted as the mini/junior version of the EDEN alliance.",
                      color=0x008000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/7/7a/Flag-GEA.png')
embed.add_field(name="Fomation", value="1486", inline=False)
embed.add_field(name="Disbanded", value="1863", inline=False)
embed.add_field(name="All time members", value="7", inline=False)
embed.add_field(name="Founders", value=":flag_al: Albania - :flag_in: India - :flag_nl: Netherlands", inline=False)
embed.add_field(name="Other members",
                value=":flag_tw: Taiwan - :flag_ar: Argentina - :flag_ba: Bosnia and Herzegovina - :flag_co: Colombia",
                inline=False)

embeds.append(embed)

embed = discord.Embed(title="EDEN", url='http://wiki.erepublik.com/index.php/Erepublik_Defence_%26_Economy_Network',
                      description="EDEN (Erepublik Defense & Economic Network) was one of two successor alliances to ATLANTIS. It was a military alliance consisting of 27 members.",
                      color=0x008000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/6/6b/Eden2.jpg')
embed.add_field(name="Fomation", value="665", inline=False)
embed.add_field(name="Disbanded", value="1994", inline=False)
embed.add_field(name="All time members", value="27", inline=False)
embed.add_field(name="Founders",
                value=":flag_hr: Croatia - :flag_fi: Finland - :flag_no: Norway - :flag_pl: Poland - :flag_ro: Romania - :flag_es: Spain - :flag_se: Sweden",
                inline=False)
embed.add_field(name="Other members",
                value=":flag_ca: Canada - :flag_gr: Greece - :flag_ba: Bosnia and Herzegovina - :flag_ch: Switzerland - :flag_us: USA - :flag_au: Australia - :flag_cn: China - :flag_it: Italy - :flag_bg: Bulgaria - :flag_ie: Ireland - :flag_ua: Ukraine - :flag_il: Israël - :flag_by: Belarus - :flag_pt: Portugal - :flag_al: Albania - :flag_tr: Turkey - :flag_nl: Netherlands - :flag_tw: Taiwan - :flag_ar: Argentina - :flag_co: Colombia",
                inline=False)

embeds.append(embed)

embed = discord.Embed(title="CoT", url='http://wiki.erepublik.com/index.php/Circle_of_Trust',
                      description="CoT (The Circle of Trust) was a military alliance consisting of 15 members.",
                      color=0xffff17)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/0/0a/Flag-CoT.png')
embed.add_field(name="Fomation", value="1676", inline=False)
embed.add_field(name="Disbanded", value="2176", inline=False)
embed.add_field(name="All time members", value="15", inline=False)
embed.add_field(name="Founders",
                value=":flag_bg:  Bulgaria - :flag_cl: Chile - :flag_ch: Switzerland - :flag_nz: New Zealand - :flag_kr: South KOrea - :flag_pe: Peru - :flag_py: Paraguay",
                inline=False)
embed.add_field(name="Other members",
                value=":flag_be: Belgium - :flag_de: Germany - :flag_id: INdonesia - :flag_jp: Japan - :flag_lt: Lithuania - :flag_mx: Mexico - :flag_mk: Macedonia - :flag_md: Moldova - :flag_ru: Russia - :flag_us: USA",
                inline=False)

embeds.append(embed)

embed = discord.Embed(title="NaN", url='http://wiki.erepublik.com/index.php/NaN',
                      description="NaN (Non Aligned Nations) was a military alliance consisting of 7 small countries.",
                      color=0x808000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120',
                 icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/b/b6/Flag-NaN.png')
embed.add_field(name="Fomation", value="1942", inline=False)
embed.add_field(name="Disbanded", value="2100", inline=False)
embed.add_field(name="All time members", value="8", inline=False)
embed.add_field(name="Founders", value=":flag_au: Australia - :flag_za: South Africa", inline=False)
embed.add_field(name="Other members",
                value=":flag_cy: Cyprus - :flag_my: Malaysia - :flag_pk: Pakistan - :flag_sa: Saudi Arabia - :flag_eg: Egypt - :flag_ph: Philippines",
                inline=False)

embeds.append(embed)

embed=discord.Embed(title="TWO", url='http://wiki.erepublik.com/index.php/The_World_is_Ours', description="TWO (The World is Ours) was a military alliance consisting of 19 members. Big countries were called TWO, and small ones were called ACT.", color=0x0065ca)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/1/17/Flag-TWO.png')
embed.add_field(name="Formation", value="1839", inline=False)
embed.add_field(name="Disbanded", value="2244", inline=False)
embed.add_field(name="All time members", value="19", inline=False)
embed.add_field(name="Founders", value=":flag_hu: Hungary - :flag_pl: Poland - :flag_rs: Serbia - :flag_es: Spain - :flag_gb: United Kingdom", inline=False)
embed.add_field(name="Other members", value=":flag_gr: Greece - :flag_lv: Latvia - :flag_ee: Estonia - :flag_ve: Venezuela - :flag_th: Thailand - :flag_me: Montenegro - :flag_sk: Slovakia - :flag_lt: Lithuania - :flag_tw: Taiwan - :flag_at: Austria - :flag_by: Belarus - :flag_au: Australia - :flag_nz: New Zealand", inline=False)

embeds.append(embed)

embed=discord.Embed(title="WOLF", url='http://wiki.erepublik.com/index.php/The_World_is_Ours', description="WOLF (World Organization of Loyalty and Freedom) was a military alliance consisting of 3 members.", color=0x00ff00)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/a/ae/Flag-Wolf.png')
embed.add_field(name="Formation", value="2101", inline=False)
embed.add_field(name="Disbanded", value="2265", inline=False)
embed.add_field(name="All time members", value="3", inline=False)
embed.add_field(name="Founders", value=":flag_pk: Pakistan - :flag_eg: Egypt - :flag_sa: Saudi Arabia", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Sirius", url='http://wiki.erepublik.com/index.php/Sirius', description="Sirius was a military alliance consisting of 8 members. The alliance was ended because screenshot was found proving Poland was requesting to join Asteria.", color=0x36a8c9)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/2/22/Flag-Sirius.jpg')
embed.add_field(name="Formation", value="2278", inline=False)
embed.add_field(name="Disbanded", value="2562", inline=False)
embed.add_field(name="All time members", value="8", inline=False)
embed.add_field(name="Founders", value=":flag_hr: Croatia - :flag_pl: Poland - :flag_es: Spain - :flag_tr: Turkey - :flag_gb: United Kingdom - :flag_us: USA", inline=False)
embed.add_field(name="Other members", value=":flag_br: Brazil - :flag_ua: Ukraine", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Aurora", url='http://wiki.erepublik.com/index.php/Aurora', description="Aurora was an alliance of nations committed to loyalty, liberty, and dignity, for all member nations.", color=0xff0080)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/2/25/Flag-Aurora.jpg')
embed.add_field(name="Formation", value="2295", inline=False)
embed.add_field(name="Disbanded", value="2595", inline=False)
embed.add_field(name="All time members", value="10", inline=False)
embed.add_field(name="Founders", value=":flag_bg: Bulgaria - :flag_cl: Chile - :flag_de: Germany - :flag_id: Indonesia - :flag_ie: Ireland - :flag_mk: Macedonia - :flag_py: Paraguay", inline=False)
embed.add_field(name="Other members", value=":flag_mx: Mexico - :flag_it: Italy - :flag_ve: Venezuela", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Leto", url='http://wiki.erepublik.com/index.php/Leto', description="It was founded after TWO was dissolved. It consisted mostly of ex-ACT or ex-proTWO smaller countries. It was an organization subsidiary of Asteria alliance.  After dissolution of Leto and Asgard, their small-sized members formed Nebula and their mid-sized members formed Orion.", color=0x400040)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://i.imgur.com/KMM8u39.jpg')
embed.add_field(name="Formation", value="2289", inline=False)
embed.add_field(name="Disbanded", value="2642", inline=False)
embed.add_field(name="All time members", value="13", inline=False)
embed.add_field(name="Founders", value=":flag_by: Belarus - :flag_co: Colombia - :flag_il: Israël - :flag_pt: Portugal - :flag_tw: Taiwan - :flag_md: Moldova", inline=False)
embed.add_field(name="Other members", value=":flag_ca: Canada - :flag_fr: France - :flag_ir: Iran - :flag_pe: Peru - :flag_me: Montenegro - :flag_au: Australia - :flag_cz: Czech Republic ", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Asgard", url='http://wiki.erepublik.com/index.php/Asgard', description="Asgard was founded by Sweden and Finland with the aim to strengthen the Nordic brotherhood and to give the fate of the nations in Asgard into their own hands. Norway took part in the early discussions and plans of creating a local Northern Alliance but decided not to go through with it and instead stayed with their alliance at the time, EDEN.", color=0xc0c0c0)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/9/9b/Flag-Asgard.jpg')
embed.add_field(name="Formation", value="1737", inline=False)
embed.add_field(name="Disbanded", value="2648", inline=False)
embed.add_field(name="All time members", value="4", inline=False)
embed.add_field(name="Founders", value=":flag_se: Sweden - :flag_fi: Finland", inline=False)
embed.add_field(name="Other members", value=":flag_ca: Canada - :flag_no: Norway", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Root", url='http://wiki.erepublik.com/index.php/Root', description="Root was a military alliance consisting of 5 countries.", color=0xffffff)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/b/bc/Flag-Root.jpg')
embed.add_field(name="Formation", value="2437", inline=False)
embed.add_field(name="Disbanded", value="2703", inline=False)
embed.add_field(name="All time members", value="8", inline=False)
embed.add_field(name="Founders", value=":flag_sk: Slovakia - :flag_kr: South Korea - :flag_ch: Switzerland - :flag_lt: Lithuania - :flag_ee: Estonia - :flag_ba: Bosnia and Herzegovina", inline=False)
embed.add_field(name="Other members", value=":flag_ge: Georgia - :flag_al: Albania - :flag_by: Belarus", inline=False)

embeds.append(embed)

embed=discord.Embed(title="P.L.U.T.O.", url='http://wiki.erepublik.com/index.php/P.L.U.T.O.', description="P.L.U.T.O. (also called PLUTO) was a military alliance consisting of 7 countries.", color=0xffffff)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/8/8b/Flag-P.L.U.T.O..jpg')
embed.add_field(name="Formation", value="2932", inline=False)
embed.add_field(name="Disbanded", value="3222", inline=False)
embed.add_field(name="All time members", value="7", inline=False)
embed.add_field(name="Founders", value=":flag_be: Belgium - :flag_es: Spain - :flag_gb: United Kingdom", inline=False)
embed.add_field(name="Other members", value=":flag_kr: South Korea - :flag_mx: Mexico - :flag_py: Paraguay - :flag_bo: Bolivia", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Syndicates", url='http://wiki.erepublik.com/index.php/Syndicate', description="Syndicate was a military alliance founded as an anti-Asteria alliance", color=0xff8040)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/e/e3/Flag-Syndicate.jpg')
embed.add_field(name="Formation", value="3095", inline=False)
embed.add_field(name="Disbanded", value="3446", inline=False)
embed.add_field(name="All time members", value="8", inline=False)
embed.add_field(name="Founders", value=":flag_ar: Argentina - :flag_br: Brazil - :flag_gr: Greece - :flag_tr: Turkey", inline=False)
embed.add_field(name="Other members", value=":flag_cl: Chile - :flag_ua: Ukraine - :flag_it: Italy - :flag_hr: Croatia ", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Adriatica", url='http://wiki.erepublik.com/index.php/Adriatica', description="Adriatica was started with the idea of joining anti-Asteria countries, however, within few months all major members left to join Syndicate. Several small countries joined afterwards.", color=0x804000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/0/0e/Flag-Adriatica.png')
embed.add_field(name="Formation", value="3051", inline=False)
embed.add_field(name="Disbanded", value="3443", inline=False)
embed.add_field(name="All time members", value="10", inline=False)
embed.add_field(name="Founders", value=":flag_hr: Croatia", inline=False)
embed.add_field(name="Other members", value=":flag_ve: Venezuela - :flag_th: Thailand - :flag_ge: Georgia - :flag_it: Italy - :flag_al: Albania - :flag_cl: Chile - :flag_cy: Cyprus - :flag_ie: Ireland - :flag_mx: Mexico", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Orion", url='http://wiki.erepublik.com/index.php/Orion', description="Orion is a medium-sized alliance, friendly to Asteria. It was founded after Leto was dissolved.", color=0x0000a0)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/1/11/Flag-Orion.jpg')
embed.add_field(name="Formation", value="2713", inline=False)
embed.add_field(name="Disbanded", value="Still running", inline=False)
embed.add_field(name="All time members", value="11", inline=False)
embed.add_field(name="Founders", value=":flag_ca: Canada - :flag_fr: France - :flag_co: Colombia - :flag_ir: Iran - :flag_pr: Peru - :flag_se: Sweden", inline=False)
embed.add_field(name="Other members", value=":flag_nl: Netherlands - :flag_lt: Lithuania - :flag_cu: Cuba - :flag_gb: United Kingdom - :flag_ee: Estonia", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Nebula", url='http://wiki.erepublik.com/index.php/Nebula', description="As outlined in the Nebula alliance charter, Nebula's primary objectives are to defend and protect each member country against foreign invaders and to fight for Asteria and its allies.", color=0x979700)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/7/71/Flag-Nebula.png')
embed.add_field(name="Formation", value="2671", inline=False)
embed.add_field(name="Disbanded", value="Still running", inline=False)
embed.add_field(name="All time members", value="8", inline=False)
embed.add_field(name="Founders", value=":flag_au: Australia - :flag_il: Israël - :flag_me: Montenegro - :flag_jp: Japan - :flag_no: Norway", inline=False)
embed.add_field(name="Other members", value=":flag_cz: Czech Republic - :flag_uy: Uruguay - :flag_at: Austria", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Pacifca", url='http://wiki.erepublik.com/index.php/Pacifica_(alliance)', description="It was a medium-size alliance until Poland and Hungary joined it in April 2016, which then turned it into one of the major alliances in the game. It has mostly followed the path of neutrality between Asteria and Syndicate since, keeping MPPs with both sides and avoiding major conflicts", color=0xdf0005)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/0/02/Flag-Pacifica.jpg')
embed.add_field(name="Formation", value="2403", inline=False)
embed.add_field(name="Disbanded", value="Still running", inline=False)
embed.add_field(name="All time members", value="13", inline=False)
embed.add_field(name="Founders", value=":flag_ru: Rusia - :flag_us: USA", inline=False)
embed.add_field(name="Other members", value=":flag_lv: Latvia - :flag_tw: Taiwan - :flag_fi: Finland - :flag_co: Colombia - :flag_se: Sweden - :flag_gr: Greece - :flag_hu: Hungary - :flag_pl: Poland - :flag_ar: Argentina - :flag_br: Brazil - :flag_mx: Mexico", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Asteria", url='http://wiki.erepublik.com/index.php/Asteria', description="Asteria is a military alliance founded after TWO was dissolved.", color=0xff0000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='https://s10.postimg.org/m37o1jxa1/image.png')
embed.add_field(name="Formation", value="2275", inline=False)
embed.add_field(name="Disbanded", value="Still running", inline=False)
embed.add_field(name="All time members", value="12", inline=False)
embed.add_field(name="Founders", value=":flag_ar: Argentina - :flag_gr: Greece - :flag_hu: Hungary - :flag_ro: Romania - :flag_rs: Serbia - :flag_si: Slovenia", inline=False)
embed.add_field(name="Other members", value=":flag_cn: China - :flag_br: Brazil - :flag_pt: Portugal - :flag_pr: Peru - :flag_ir: Iran - :flag_lt: Lithuania", inline=False)

embeds.append(embed)

embed=discord.Embed(title="Andes", url='http://wiki.erepublik.com/index.php/Andes', description="Andes is an alliance of six countries from South America", color=0x800000)
embed.set_author(name="azaraliiii#4764", url='https://discordapp.com/channels/@me/344531696479109120', icon_url='http://forum.erepfrance.com/download/file.php?avatar=8004_1497794429.png')
embed.set_thumbnail(url='http://wiki.erepublik.com/images/1/10/Flag-Andes.png')
embed.add_field(name="Formation", value="3474", inline=False)
embed.add_field(name="Disbanded", value="Still running", inline=False)
embed.add_field(name="All time members", value="6", inline=False)
embed.add_field(name="Founders", value=":flag_ve: Venezuela - :flag_cl: Chile - :flag_uy: Uruguay - :flag_bo: Bolivia", inline=False)
embed.add_field(name="Other members", value=":flag_ar: Argentina - :flag_py: Paraguay", inline=False)

embeds.append(embed)

jsonembeds = []

for em in embeds:
    jsonembeds.append((json.JSONEncoder().encode(em.to_dict()), em.title))

conn = sqlite3.connect('erep.db')
c = conn.cursor()
c.execute('CREATE TABLE wiki(id INTEGER PRIMARY KEY, tag TEXT, category TEXT, embed TEXT)')

for jem in jsonembeds:
    c.execute('INSERT INTO wiki(tag, category, embed) VALUES (?,?,?)', (jem[1], 'Alliance', jem[0]))

conn.commit()
conn.close()
