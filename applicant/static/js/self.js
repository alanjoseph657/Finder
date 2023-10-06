function launch_toast() {
    var x = document.getElementById("toast")
    //getting the DIV
    x.className = "show";
    //adding show to DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
    //removing show after 5sec
}

