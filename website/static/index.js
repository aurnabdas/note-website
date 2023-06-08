function deleteNote(noteId){
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({noteID: noteId})
    }).then((_res) => {
        window.location.href - "/";
    })
} 
// its going to take the note id that is passed and its going to send a post request
// to the delete note endpoint. then when it gets a response it is going to reload the
//window using window.location.href - "/";.
