# =========================================================
# JAWA TENGAH REGION DATABASE - FINAL FIXED VERSION
# =========================================================

import re

JATENG_REGIONS = {

    "Kabupaten Banjarnegara": {
        "aliases": ["banjarnegara"],
        "kecamatan": ["Banjarmangu","Banjarnegara","Batur","Kalibening","Karangkobar",
        "Madukara","Mandiraja","Pagedongan","Pagentan","Pandanarum",
        "Pejawaran","Purwanegara","Punggelan","Rakit","Sigaluh",
        "Susukan","Wanadadi","Wanayasa"]
    },

    "Kabupaten Banyumas": {
        "aliases": ["banyumas","purwokerto"],
        "kecamatan": ["Ajibarang","Baturaden","Cilongok","Kalibagor","Karanglewas",
        "Kedungbanteng","Kembaran","Kemranjen","Lumbir","Patikraja",
        "Pekuncen","Purwojati","Purwokerto Barat","Purwokerto Selatan",
        "Purwokerto Timur","Purwokerto Utara","Rawalo","Sokaraja",
        "Somagede","Sumbang","Sumpiuh","Tambak","Wangon"]
    },

    "Kabupaten Batang": {
        "aliases": ["batang"],
        "kecamatan": ["Bandar","Banyuputih","Batang","Blado","Gringsing",
        "Kandeman","Limpung","Pecalungan","Reban","Subah",
        "Tersono","Tulis","Warungasem"]
    },

    "Kabupaten Blora": {
        "aliases": ["blora"],
        "kecamatan": ["Banjarejo","Blora","Bogorejo","Cepu","Japah","Jati",
        "Jepon","Jiken","Kedungtuban","Kradenan","Kunduran",
        "Ngawen","Randublatung","Sambong","Todanan","Tunjungan"]
    },

    "Kabupaten Boyolali": {
        "aliases": ["boyolali"],
        "kecamatan": ["Ampel","Andong","Banyudono","Boyolali","Cepogo","Gladagsari",
        "Juwangi","Karanggede","Kemusu","Klego","Mojosongo",
        "Musuk","Nogosari","Sambi","Sawit","Selo","Simoboyo",
        "Teras","Wonosegoro"]
    },

    "Kabupaten Brebes": {
        "aliases": ["brebes"],
        "kecamatan": ["Banjarharjo","Bantarkawung","Brebes","Bulakamba","Bumiayu",
        "Jatibarang","Kersana","Ketanggungan","Larangan","Losari",
        "Paguyangan","Salem","Sirampog","Songgom","Tanjung","Tonjong","Wanasari"]
    },

    "Kabupaten Cilacap": {
        "aliases": ["cilacap"],
        "kecamatan": ["Adipala","Bantarsari","Binangun","Cilacap Selatan","Cilacap Tengah",
        "Cilacap Utara","Cimanggu","Cipari","Dayeuhluhur","Gandrungmangu",
        "Jeruklegi","Kampung Laut","Karangpucung","Kawunganten","Kedungreja",
        "Kesugihan","Kroya","Majenang","Maos","Nusawungu","Patimuan",
        "Sampang","Sidareja","Wanareja"]
    },

    "Kabupaten Demak": {
        "aliases": ["demak"],
        "kecamatan": ["Bonang","Demak","Dempet","Gajah","Guntur","Karanganyar",
        "Karangawen","Karangtengah","Kebonagung","Mijen",
        "Mranggen","Sayung","Wedung","Wonosalam"]
    },

    "Kabupaten Grobogan": {
        "aliases": ["grobogan","purwodadi"],
        "kecamatan": ["Brati","Gabus","Geyer","Godong","Grobogan","Gubug",
        "Karangrayung","Kedungjati","Klambu","Kradenan",
        "Ngaringan","Penawangan","Pulokulon","Purwodadi",
        "Tanggungharjo","Tawangharjo","Tegowanu","Toroh","Wirosari"]
    },

    "Kabupaten Jepara": {
        "aliases": ["jepara"],
        "kecamatan": ["Bangsri","Batealit","Donorojo","Jepara","Kalinyamatan",
        "Karimunjawa","Kedung","Keling","Kembang","Mayong",
        "Mlonggo","Nalumsari","Pakis Aji","Pecangaan","Tahunan","Welahan"]
    },

    "Kabupaten Karanganyar": {
        "aliases": ["karanganyar"],
        "kecamatan": ["Colomadu","Gondangrejo","Jaten","Jatipuro","Jatiyoso",
        "Jenawi","Karanganyar","Karangpandan","Kebakkramat",
        "Kerjo","Matesih","Ngargoyoso","Tasikmadu","Tawangmangu"]
    },

    "Kabupaten Kebumen": {
        "aliases": ["kebumen"],
        "kecamatan": ["Adimulyo","Alian","Ambal","Ayah","Bonorowo","Buayan",
        "Buluspesantren","Gombong","Karanganyar","Karanggayam",
        "Karangsambung","Kebumen","Klirong","Kutowinangun",
        "Kuwarasan","Mirit","Padureso","Pejagoan","Petanahan",
        "Poncowarno","Prembun","Puring","Rowokele","Sadang","Sempor","Sruweng"]
    },

    "Kabupaten Kendal": {
        "aliases": ["kendal"],
        "kecamatan": ["Boja","Brangsong","Cepiring","Gemuh","Kaliwungu",
        "Kaliwungu Selatan","Kangkung","Kendal","Limbangan",
        "Ngampel","Pagerruyung","Patean","Patebon","Pegandon",
        "Plantungan","Ringinarum","Rowosari","Singorojo","Sukorejo","Weleri"]
    },

    "Kabupaten Klaten": {
        "aliases": ["klaten"],
        "kecamatan": ["Bayat","Cawas","Ceper","Delanggu","Gantiwarno","Jatinom",
        "Jogonalan","Juwiring","Kalikotes","Karanganom","Karangdowo",
        "Karangnongko","Kebonarum","Kemalang","Klaten Selatan",
        "Klaten Tengah","Klaten Utara","Manisrenggo","Ngawen",
        "Pedan","Polanharjo","Prambanan","Trucuk","Tulung","Wedi","Wonosari"]
    },

    "Kabupaten Kudus": {
        "aliases": ["kudus"],
        "kecamatan": ["Bae","Dawe","Gebog","Jati","Jekulo","Kaliwungu","Kudus","Mejobo","Undaan"]
    },

    "Kabupaten Magelang": {
        "aliases": ["kab magelang"],
        "kecamatan": ["Bandongan","Borobudur","Candimulyo","Dukun","Grabag",
        "Kajoran","Kaliangkrik","Mertoyudan","Mungkid","Muntilan",
        "Ngablak","Ngluwar","Pakis","Salam","Salaman",
        "Sawangan","Secang","Srumbung","Tegalrejo","Tempuran","Windusari"]
    },

    "Kabupaten Pati": {
        "aliases": ["pati"],
        "kecamatan": ["Batangan","Cluwak","Dukuhseti","Gabus","Gembong","Gunungwungkal",
        "Jaken","Jakenan","Juwana","Kayen","Margorejo","Margoyoso",
        "Pati","Pucakwangi","Sukolilo","Tambakromo","Tayu","Trangkil","Wedarijaksa","Winong"]
    },

    "Kabupaten Pekalongan": {
        "aliases": ["kab pekalongan"],
        "kecamatan": ["Bojong","Buaran","Doro","Kajen","Kandangserang",
        "Karanganyar","Karangdadap","Kedungwuni","Kesesi",
        "Lebakbarang","Paninggaran","Petungkriyono",
        "Siwalan","Sragi","Talun","Tirto","Wiradesa","Wonokerto"]
    },

    "Kabupaten Pemalang": {
        "aliases": ["pemalang"],
        "kecamatan": ["Ampelgading","Bantarbolang","Belik","Bodeh","Comal",
        "Moga","Pemalang","Petarukan","Pulosari","Randudongkal",
        "Taman","Ulujami","Warungpring","Watukumpul"]
    },

    "Kabupaten Purbalingga": {
        "aliases": ["purbalingga"],
        "kecamatan": ["Bobotsari","Bojongsari","Bukateja","Kaligondang","Kalimanah",
        "Karanganyar","Karangjambu","Karangmoncol","Karangreja",
        "Kejobong","Kemangkon","Kertanegara","Kutasari",
        "Mrebet","Padamara","Pengadegan","Purbalingga","Rembang"]
    },

    "Kabupaten Purworejo": {
        "aliases": ["purworejo"],
        "kecamatan": ["Bagelen","Banyuurip","Bayan","Bener","Bruno",
        "Butuh","Gebang","Grabag","Kaligesing","Kemiri",
        "Kutoarjo","Loano","Ngombol","Pituruh","Purwodadi","Purworejo"]
    },

    "Kabupaten Rembang": {
        "aliases": ["rembang"],
        "kecamatan": ["Bulu","Gunem","Kaliori","Kragan","Lasem",
        "Pamotan","Pancur","Rembang","Sale","Sarang","Sedan","Sluke","Sulang"]
    },

    "Kabupaten Semarang": {
        "aliases": ["kab semarang","ungaran"],
        "kecamatan": ["Ambarawa","Bancak","Bandungan","Banyubiru","Bawen",
        "Bergas","Bringin","Getasan","Jambu","Kaliwungu",
        "Pabelan","Pringapus","Sumowono","Suruh","Susukan",
        "Tengaran","Tuntang","Ungaran Barat","Ungaran Timur"]
    },

    "Kabupaten Sragen": {
        "aliases": ["sragen"],
        "kecamatan": ["Gemolong","Gesi","Gondang","Jenar","Kalijambe",
        "Karangmalang","Kedawung","Masaran","Miri","Mondokan",
        "Ngrampal","Plupuh","Sambirejo","Sambungmacan",
        "Sidoharjo","Sragen","Sukodono","Tangen","Tanon"]
    },

    "Kabupaten Sukoharjo": {
        "aliases": ["sukoharjo"],
        "kecamatan": ["Baki","Bendosari","Bulu","Gatak","Grogol",
        "Kartasura","Mojolaban","Nguter","Polokarto",
        "Sukoharjo","Tawangsari","Weru"]
    },

    "Kabupaten Tegal": {
        "aliases": ["kab tegal"],
        "kecamatan": ["Adiwerna","Balapulang","Bojong","Bumijawa","Dukuhturi",
        "Dukuhwaru","Jatinegara","Kedungbanteng","Kramat",
        "Lebaksiu","Margasari","Pagerbarang","Pangkah",
        "Slawi","Suradadi","Talang","Tarub","Warureja"]
    },

    "Kabupaten Temanggung": {
        "aliases": ["temanggung"],
        "kecamatan": ["Bansari","Bejen","Bulu","Candiroto","Gemawang",
        "Jumo","Kaloran","Kandangan","Kedu","Kledung",
        "Kranggan","Ngadirejo","Parakan","Pringsurat",
        "Selopampang","Temanggung","Tembarak","Tlogomulyo","Tretep","Wonoboyo"]
    },

    "Kabupaten Wonogiri": {
        "aliases": ["wonogiri"],
        "kecamatan": ["Batuwarno","Baturetno","Bulukerto","Eromoko","Girimarto",
        "Giritontro","Giriwoyo","Jatipurno","Jatiroto",
        "Jatisrono","Karangtengah","Kismantoro","Manyaran",
        "Ngadirojo","Nguntoronadi","Paranggupito",
        "Pracimantoro","Puhpelem","Purwantoro",
        "Selogiri","Sidoharjo","Slogohimo","Tirtomoyo",
        "Wonogiri","Wuryantoro"]
    },

    "Kabupaten Wonosobo": {
        "aliases": ["wonosobo"],
        "kecamatan": ["Garung","Kalibawang","Kalikajar","Kaliwiro","Kejajar",
        "Kepil","Kertek","Leksono","Mojotengah","Sapuran",
        "Selomerto","Sukoharjo","Wadaslintang","Watumalang","Wonosobo"]
    },

    "Kota Magelang": {
        "aliases": ["magelang kota"],
        "kecamatan": ["Magelang Selatan","Magelang Tengah","Magelang Utara"]
    },

    "Kota Pekalongan": {
        "aliases": ["pekalongan kota"],
        "kecamatan": ["Pekalongan Barat","Pekalongan Selatan","Pekalongan Timur","Pekalongan Utara"]
    },

    "Kota Salatiga": {
        "aliases": ["salatiga"],
        "kecamatan": ["Argomulyo","Sidomukti","Sidorejo","Tingkir"]
    },

    "Kota Semarang": {
        "aliases": ["semarang kota"],
        "kecamatan": ["Banyumanik","Candisari","Gajahmungkur","Gayamsari","Genuk",
        "Gunungpati","Mijen","Ngaliyan","Pedurungan","Semarang Barat",
        "Semarang Selatan","Semarang Tengah","Semarang Timur","Semarang Utara","Tembalang","Tugu"]
    },

    "Kota Surakarta": {
        "aliases": ["solo","surakarta"],
        "kecamatan": ["Banjarsari","Jebres","Laweyan","Pasar Kliwon","Serengan"]
    },

    "Kota Tegal": {
        "aliases": ["tegal kota"],
        "kecamatan": ["Margadana","Tegal Barat","Tegal Selatan","Tegal Timur"]
    }

}


# =========================
# LOCATION MATCHER ENGINE
# =========================

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text


def detect_location(text):
    text = normalize_text(text)

    # PRIORITAS 1 → kecamatan
    for region, data in JATENG_REGIONS.items():
        for kec in data.get("kecamatan", []):
            pattern = r"\b" + re.escape(kec.lower()) + r"\b"
            if re.search(pattern, text):
                return f"{kec}, {region}"

    # PRIORITAS 2 → alias kabupaten/kota
    for region, data in JATENG_REGIONS.items():
        for alias in data.get("aliases", []):
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"
            if re.search(pattern, text):
                return region

    return "Tidak Diketahui"