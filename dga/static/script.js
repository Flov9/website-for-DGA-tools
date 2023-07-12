$(document).ready(function() {
    if (window.location.pathname != null) {
        $('#upmHeaderLogo').attr('src', '../static/images/upm-logo.png')
    } else {
        $('#upmHeaderLogo').attr('src', '/static/images/upm-logo.png')
    }
})

$(function() {
    var limit = 3;

    $('.form-check-input').on('change', function(evt) {
        if($("input[name='image']:checked").length >= limit) {
            this.checked = false;
        }
    });

    $('#image-form').submit(function(e) {
        e.preventDefault();
        
        var selectedImages = $("input[name='image']:checked").map(function() {
            return $(this).val() + ".png";
        }).get();

        console.log(selectedImages);

        // Display the selected images
        $('#selected-images').empty();
        
        for (var i = 0; i < selectedImages.length; i++) {
          // Add a random query parameter to the image URL to prevent caching
          // This makes the URL unique for every request and forces the browser to fetch the new image
          var noCacheParam = new Date().getTime();
          var imageSrc = staticUrlPrefix + "images/" + selectedImages[i] + "?" + noCacheParam;
          $('#selected-images').append('<img src="' + imageSrc + '" width="500px">');
        }
    });
});

/* Handle the display of records */

$(function() {
  const recordDropdown = $(".dropdown-menu li a");
  const addNewTransformerButton = $(".modal-footer button.btn-primary");

  // Record dropdown click event handler
  recordDropdown.on("click", function(event) {
    event.preventDefault();

    $(".dropdown-toggle:first-child").text($(this).text());
    $(".dropdown-toggle:first-child").val($(this).text());

    const transformer_selected = $(this).text();
    let type = "update"; 

    $.ajax({
      url: recordsUrl,
      dataType: "json",
      method: "POST",
      data: $(this).closest("form").serialize() 
        + '&transformer_selected=' + encodeURIComponent(transformer_selected) 
        + '&type=' + encodeURIComponent(type),
      success: function(response) {
        // Iterate through the records and create card elements for each record
        let recordsHtml = "";

        for (let key in response.kt) {
          let recordKey = key;
          let timestamp = response.kt[key];

          recordsHtml += `
          <a href="#" class="card mb-2 link-underline link-underline-opacity-0 record-link"
            data-record-url="{{ url_for('rtdatabase.records') }}"
            data-record-selected="${recordKey}"
            name="${recordKey}"
            aria-current="true">
            <div class="card-body">
              <div>
                <h5 class="fw-semibold">${recordKey}</h5>
              </div>
              <small class="text-body-tertiary">
                ${timestamp}
              </small>
            </div>
          </a>
        `;
        
        }

        $("#record-list").html(recordsHtml);
      },
      error: function(xhr, status, error) {
        // Handle any errors that occur during the AJAX request
        console.log(status + ": " + error);
      }
    });
  });

  // // Add new record button click event handler
  // addNewTransformerButton.on("click", function() {
  //   const transformerName = $(this).closest("form").find("input.form-control").val();
  //   let type = "add"; // or "update" depending on the action you want to perform
  //   console.log(transformerName);

  //   $.ajax({
  //     url: recordsUrl,
  //     method: "POST",
  //     data: $(this).closest("form").serialize() + '&transformer_selected=' + encodeURIComponent(transformerName) + '&type=' + encodeURIComponent(type),
  //     success: function(response) {
  //       // ...
  //     }
  //   });
  // });
});

/* Handle the click events on a record link */

let selected_record = null;
let selected_transformer = null;

$(document).on("click", ".record-link", function(event) {
  event.preventDefault();

  selected_record = $(this).data("record-selected");
  selected_transformer = $(".dropdown-toggle:first-child").val();

  let type = "update";

  // Remove the 'selected' class from the previously selected record
  $(".record-link.selected").removeClass("selected");

  // Add the 'selected' class to the clicked record
  $(this).addClass("selected");

  // Clear the previous record's images
  $('#selected-images').empty();

  // Clear the checkbox input
  $("input[name='image']:checked").prop('checked', false);

  $.ajax({
    url: recordsUrl,
    method: "POST",
    data: $(this).closest("form").serialize() 
      + '&record_selected=' + encodeURIComponent(selected_record) 
      + '&type=' + encodeURIComponent(type) 
      + '&transformer_selected=' + encodeURIComponent(selected_transformer),
    success: function(response) {
      // ...
    }
  });
});

$('#emailButton').click(function() {
  let type = "email";

  if (selected_record == null) {
    alert("Please select a record.");
    return;
  }

  $.ajax({
    url: recordsUrl,
    method: "POST",
    data: $(this).closest("form").serialize() 
      + '&record_selected=' + encodeURIComponent(selected_record) 
      + '&type=' + encodeURIComponent(type) 
      + '&transformer_selected=' + encodeURIComponent(selected_transformer),
    success: function(response) {
      alert("Email sent successfully.")
    },
    error: function(response) {
      alert("There was an error sending the email.")
    }
  });
});

$('#deleteButton').click(function() {
  let type = "delete";

  if (selected_record == null) {
    alert("Please select a record.");
    return;
  }

  $.ajax({
    url: recordsUrl,
    method: "POST",
    data: $(this).closest("form").serialize() 
      + '&record_selected=' + encodeURIComponent(selected_record) 
      + '&type=' + encodeURIComponent(type) 
      + '&transformer_selected=' + encodeURIComponent(selected_transformer),
    success: function(response) {
      sessionStorage.setItem('deleted', 'true'); // set the flag
      location.reload();
    },
    error: function(response) {
      alert("There was an error deleting the record.")
    }
  });
});

// When the page loads, check for the flag
$(document).ready(function() {
  if (sessionStorage.getItem('deleted') === 'true') {
    alert("Record deleted successfully.")
    sessionStorage.removeItem('deleted'); // clear the flag
  }
});