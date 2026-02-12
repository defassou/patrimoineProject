document.querySelector('form').addEventListener('submit', function(event) {
    const date_de_debut = document.querySelector('#id_date_debut').value;
    const date_de_fin = document.querySelector('#id_date_fin').value;

    if (new Date(date_de_debut) > new Date(date_de_fin)) {
        alert("La date de début doit être avant la date de fin.");
        event.preventDefault();
    }
});
