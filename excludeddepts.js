let excludedDepartments= [ // matched case-insensitively ANYWHERE in a home-institute address, clean rows only (NS not marked *)
"Inst Hlth Sci",   // the Ph.D. institute. safe unanchored, the filter only tests home institute segments
"Vocat Sch Hlth Sci",
"Physiocare Rehabil Ctr",
"Food Proc, Food Technol",
"Fac Sci & Letters",
"Dept Nutr & Dietet",
"Dept Exercise & Sport Sci",
"Psychiat Nursing",
"Comp Engn",
"Elect & Elect Engn",
"Elekt Elekt Muhendisligi",
"Elekt & Elekt Muhendis",
"Biomed Engn",
"Biyomed Muhendisligi",
"Fac Eng",
"Mech Engn",
"Ind Engn",
"Bilgisayar Muhendisligi",
"Muhendislik Fak",
// Dental entries match the DEPARTMENT, never "Fac Dent". Wos sometimes prints "Fac Dent" on a
// medical record (e.g. "Fac Dent, Dept Thorac Surg") and sometimes prints "Fac Med" on a dental
// one (e.g. "Fac Med, Dept Periodontol"), so the department is the field that can be trusted.
"Maxillofacial",        // also catches Dentomaxillofacial and Oral & Maxillofacial
"Periodontol",
"Orthodont",
"Pediat Dent",
"Endodont",
"Prosthodont",
"Restorat Dent",
"Dent Clin",
"Oral Dent",
"Agiz Dis",             // Agiz Dis & Cene Cerrahisi Anabilim Dali
"Ortodonti",
];

let protectedNames= [ // medical faculty, e.g. attending a Ph.D. at Inst Hlth Sci, never dropped by department
"Atac, Fatma Belgin",
"Erdem, S. Remzi",
"Kibaroglu, Seda",
"Verdi, Hasibe",
"Bilgili, Gamze Ozcurumez",
"Hatipoglu, Ahmet",
"Topkan, Erkan",
"Terzi, Aysen",
"Turnaoglu, Hale",
"Bozalioglu, Sema",
];
