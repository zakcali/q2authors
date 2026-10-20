let nameDictAddresses= [ // a short name that fits several people, resolved by a word in the row's address
// applied after namedict.js, to clean rows only (NS not marked *). the name is replaced only when the address
// matches exactly one entry: an address matching two people, or none, keeps the short name.
// words are matched case-insensitively anywhere in the address, like excludeddepts.js
// wos (optional): publications checked by hand. the short name on these is this person, whatever the address
{name: "Haberal, Mehmet",      shortnames: ["Haberal, M", "Haberal, M."], addresses: ["Transplant", "Gen Surg", "Dept Surg"],
	wos: ["WOS:000252037900055", "WOS:000252037900066"]}, // 2008, Dept Radiol address
{name: "Haberal, Kemal Murat", shortnames: ["Haberal, M", "Haberal, M."], addresses: ["Radiol", "Radiodiag"]},
];
