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

        // Display the selected images
        $('#selected-images').empty();
        
        for (var i = 0; i < selectedImages.length; i++) {
            var imageSrc = staticUrlPrefix + "images/" + selectedImages[i];
            $('#selected-images').append('<img src="' + imageSrc + '" width="500px">');
        }
    });
});

// script for record page

$(function() {
  const recordDropdown = $(".dropdown-menu li a");
  const addNewTransformerButton = $(".modal-footer button.btn-primary");

  // Record dropdown click event handler
  recordDropdown.on("click", function(event) {
    event.preventDefault();

    $(".btn:first-child:not(.navbar-btn)").text($(this).text());
    $(".btn:first-child:not(.navbar-btn)").val($(this).text());

    const transformer_selected = $(this).text();
    console.log(transformer_selected);
    let type = "update"; 

    $.ajax({
      url: recordsUrl,
      dataType: "json",
      method: "POST",
      data: $(this).closest("form").serialize() + '&transformer_selected=' + encodeURIComponent(transformer_selected) + '&type=' + encodeURIComponent(type),
      success: function(response) {
        // Iterate through the records and create card elements for each record
        let recordsHtml = "";

        console.log("test message")
        console.log(response.kt)

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

  // Add new record button click event handler
  addNewTransformerButton.on("click", function() {
    const transformerName = $(this).closest("form").find("input.form-control").val();
    let type = "add"; // or "update" depending on the action you want to perform
    console.log(transformerName);

    $.ajax({
      url: recordsUrl,
      method: "POST",
      data: $(this).closest("form").serialize() + '&transformer_selected=' + encodeURIComponent(transformerName) + '&type=' + encodeURIComponent(type),
      success: function(response) {
        // ...
      }
    });
  });
});

$(document).on("click", ".record-link", function(event) {
  event.preventDefault();

  const recordSelected = $(this).data("record-selected");
  const transformer_selected = $(".btn:first-child:not(.navbar-btn)").val();

  let type = "update";

  $.ajax({
    url: recordsUrl,
    method: "POST",
    data: $(this).closest("form").serialize() + '&record_selected=' + encodeURIComponent(recordSelected) + '&type=' + encodeURIComponent(type) + '&transformer_selected=' + encodeURIComponent(transformer_selected),
    success: function(response) {
      // Redirect the user to the desired URL
      window.location.href = `/records`;
    }
  });
});

