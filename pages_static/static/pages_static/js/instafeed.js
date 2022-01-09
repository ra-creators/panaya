let customTemplate = 
`
<div class="item"
onClick=instaModal("{{model.permalink}}")
>
<div class="card">
    <img class="hov2"
      src="{{image}}"
      loading="lazy"
      class="card-img-top"
      alt="..."
    />
  <div class="hover_part2"></div>
</div>
</div>
`
let instaModal = (data)=>{
    // console.log(data)
    // post = event.target.dataset.post
    // console.log('clicked', event.target, event.target.dataset, post)
    var myModal = new bootstrap.Modal(document.getElementById('instaPostModal'), )
    let instaIframe = document.getElementById('instaIframe')
    instaIframe.src = data+'embed'
    myModal.show()
}

// let instaContainer = document.getElementById("instafeed")
// instaContainer.onchange(e=>console.log('ehi'))
    
var feed = new Instafeed({
accessToken: 'IGQVJVUFh5MUpWTUI2NEJZAMnZAXbnY0X0JRbGwySUlGVWFRWmtBeExXaExPZAkNUX3NPbXRRS1JPSDRPc3g3NmZA2VFBaSFhyWFk4ZAlYwNFFOYkZAhRVlBUHVyS3Vka09BdlRPZAExmWVVlbnZAuUTNOejIwOAZDZD',
template: customTemplate,
after: () => $("#instafeed").owlCarousel({
    nav: true,
    // loop: true,
    margin: 10,
    dots: false,
    lazyLoad: true,
    autoplay: true,
    lazyLoadEager: 2,
    responsive: {
      0: {
        items: 1,
      },
      800: {
        items: 2,
      },
      1200: {
        items: 3,
      },
    },
  }),
});
feed.run();

$(".owl-item").owlCarousel({
    nav: true,
  // loop: true,
  margin: 10,
  lazyLoad: true,
  autoplay: true,
  lazyLoadEager: 3,
  responsive: {
    0: {
      items: 1,
    },
    800: {
      items: 2,
    },
    1200: {
      items: 3,
    },
  },
});

  $('#contact-send-button').click(function(e) {
    e.preventDefault();
    $.ajax({
        url: "{% url 'contact_us' %}",
        type: "POST",
        data: {
            'email': $('#contact-email').val(),
            'phone': $('#contact-phone').val(),
            'remarks': $('#contact-remarks').val(),
            "name": $('#contact-name').val(),
        },
        success: function(response) {
            if (response == 200) {
                alert("Contact Information Sent!");
            } else {
                alert('Error');
            }
        },
        error: function(response) {
            alert("Error");
        }
    });
});