function Anciennete(date_jour, date_embauche) {
    var embauche = new Date(date_embauche);
    return new Date(date_jour).getFullYear() - embauche.getFullYear();
}

function Age(date_naissance, date_jour) {
    var birthday = new Date(date_naissance);
    return new Date(date_jour).getFullYear() - birthday.getFullYear();
}

function NbJour(date_de_debut, date_de_fin) {
    var debut = new Date(date_de_debut);
    var fin = new Date(date_de_fin);
    return new fin.getFullYear() - debut.getFullYear();
}