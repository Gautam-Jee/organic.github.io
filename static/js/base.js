

        let slideIndex = 1;
        let slidesIndex = 0;
        showSlides(slideIndex);
        showSlide();
        // Next/previous controls
        function plusSlides(n) {
            showSlides(slideIndex += n);
        }


        function showSlides(n) {
            let i;
            let slides = document.getElementsByClassName("mySlides");
            if (n > slides.length) { slideIndex = 1 }
            if (n < 1) { slideIndex = slides.length }
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }

            slides[slideIndex - 1].style.display = "block";


        }

        function showSlide() {

            let i;
            let slides = document.getElementsByClassName("mySlides");
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }
            slidesIndex++;
            if (slidesIndex > slides.length) { slidesIndex = 1 }

            slides[slidesIndex - 1].style.display = "block";
            setTimeout(showSlide, 10000); // Change image every 10 seconds
        }

        // for burger 

        function myFunction() {
            var x = document.getElementById("burger");
            if (x.style.display == "block") {
                x.style.display = "none";
            } else {
                x.style.display = "block";
            }

            var z = document.getElementById("bicon");
            if (z.style.display == "block") {
                z.style.display = "none";
            } else {
                z.style.display = "block";
            }
            var y = document.getElementById("cross");
            if (y.style.display == "block") {
                y.style.display = "none";
            } else {
                y.style.display = "block";
            }
        }

    // for adding address

    function addFunction() {
        var x = document.getElementById("form");
        if (x.style.display == "block") {
            x.style.display = "none";
        } else {
            x.style.display = "block";
        }
    }

   