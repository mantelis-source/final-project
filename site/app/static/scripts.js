// Functions used to perform actions with
// to-do list items
function removeItem(id) {
    // remove item from database by id
    fetch('/remove-todo', {
        method: "POST",
        body: JSON.stringify({
            itemId: id
        })
    }).then((_res) => {
        // redirect to path
        window.location.href = "/"
    })
}

function updateItemStatus(id) {
    // update item status
    fetch('/update-todo', {
        method: "POST",
        body: JSON.stringify({
            itemId: id
        })
    }).then((_res) => {
        // redirect to path
        window.location.href = "/"
    })
}