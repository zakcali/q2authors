let nameDictAddresses= [ // a short name that fits several people, resolved by a word in the row's address
// applied after namedict.js, to clean rows only (NS not marked *). the name is replaced only when the address
// matches exactly one entry: an address matching two people, or none, keeps the short name.
// words are matched case-insensitively anywhere in the address, like excludeddepts.js
// wos (optional): publications checked by hand. the short name on these is this person, whatever the address
// {name: "", shortnames: [""], addresses: [""]},
{name: "Haberal, Mehmet",      shortnames: ["Haberal, M", "Haberal, M."], addresses: ["Transplant", "Gen Surg", "Dept Surg"],
	wos: ["WOS:000252037900055", "WOS:000252037900066"]}, // 2008, Dept Radiol address
{name: "Haberal, Kemal Murat", shortnames: ["Haberal, M", "Haberal, M."], addresses: ["Radiol", "Radiodiag"]},
{name: "Onal, Cem", shortnames: ["Onal, C.", "Onal, H."], addresses: ["Radiat Oncol", "Adana"],
        wos: ["WOS:000892639300510", "WOS:000892639300509", "WOS:000892639300167", "WOS:000892639300511", "WOS:000489290100040", "WOS:000892639300451"]},
{name: "Arslan, Gulnaz", shortnames: ["Arslan, G."], addresses: ["Anesthesiol"]},
{name: "Oksuz, Ergun", shortnames: ["Oksuz, E."], addresses: ["Family Med"]},
{name: "Colak, Turan", shortnames: ["Colak, T."], addresses: ["Nephrol"]},
{name: "Yildirir, Aylin", shortnames: ["Yildirir, A."], addresses: ["Cardiol"]},
{name: "Torun, Nese", shortnames: ["Torun, N."], addresses: ["Nucl Med"]},
{name: "Dursun, Polat", shortnames: ["Dursun, P."], addresses: ["Obstet & Gynecol"]},
{name: "Seckin, Deniz", shortnames: ["Seckin, D."], addresses: ["Dermatol"]},
{name: "Erol, Ilknur", shortnames: ["Erol, I.", "Erol, I"], addresses: ["Pediat Neurol", "Ped Neurol", "Child Neurol", "Dept Pediat"]},
{name: "Haberal, Aysegul", shortnames: ["Haberal, A."], addresses: ["Biochem"], wos: ["WOS:000208702500304"]},
{name: "Haberal, Ali", shortnames: ["Haberal, A."], addresses: ["Obstet & Gynecol", "Gynecol", "Gyneacol"], wos: ["WOS:000257282500005"]},
{name: "Parlakgumus, Alper", shortnames: ["Parlakgumus, A."], addresses: ["Gen Surg"]},
{name: "Avci, Begum", shortnames: ["Avci, B."], addresses: ["Pediat Nephrol"]},
];
