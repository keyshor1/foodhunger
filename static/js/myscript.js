let submenu = document.getElementById("submenu");

    function toggleMenu(){
        submenu.classList.toggle("open-menu");
    }

let subitems = document.getElementById("subitems");

    function toggleItems(){
        subitems.classList.toggle("open-items");
    }   

    
$('#slider1, #slider2, #slider3, #slider4, #slider5').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: false,
            autoplay: true,
        },
        1000: {
            items: 4,
            nav: false,
            autoplay: true,
        },
    }
})

$(' #sliderblogs').owlCarousel({
    loop: true,
    responsiveClass: true,
    margin: 20,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: false,
            autoplay: true,
        },
        1000: {
            items: 3,
            nav: false,
            autoplay: true,
        },
    }
})

$('#sliderreview').owlCarousel({
    loop: true,
    responsiveClass: true,
    margin: 20,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: false,
            autoplay: true,
        },
        1000: {
            items: 4,
            nav: false,
            autoplay: true,
        },
    }
})

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data = ",data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

