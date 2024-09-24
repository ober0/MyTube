function open_profile(user_id){
    window.location.href = '/users/' + user_id
}

document.addEventListener('DOMContentLoaded', function (){
    let searchIsFocus = false
    document.getElementById('search-input').addEventListener('focus', function () {
        searchIsFocus = true
    })
    document.getElementById('search-input').addEventListener('blur', function () {
        searchIsFocus = false
    })

    document.addEventListener('keydown', function (event) {
        if (searchIsFocus){
            if (event.key === 'Enter' ){
                document.getElementById()
            }
        }

    })


})