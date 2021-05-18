document.querySelector(".add-button").addEventListener("click", (e) => {
  const n = document.querySelector(".all-columns>div").innerHTML;
  $(".all-columns").append(`<div>${n}</div>`);
});


$(document).on("change", ".my-selector", function () {
  if ($(this).children("option:selected").val() === "integer") {
    
      $(this).parent().next(".range").append(`
        <div class="row">
            <div class="col-6">
                <label class="form-label">From</label>
                <input name="from" type="number" class="form-control">
            </div>
            <div class="col-6">
                <label class="form-label">To</label>
                <input name="to" type="number" class="form-control">
             </div>    
        </div>`)
    ;
  }
  else{
    $(this).parent().next(".range").empty()
  }
});

$(document).on("click",'.delete-button',function(){
    if($('.delete-button').length>1){
        $(this).parentsUntil(".for-delete").remove()
    }
    
})



