$(function() {
    var nav_bar = $(".bar-nav")
    var nav = $(".aside")
    var init = function () {
        nav_bar.click(function () {
            nav.hide()
        })
    }

    init()
})