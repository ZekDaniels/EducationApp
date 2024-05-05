// Assigning Elements
const request = new Request(csrfToken);

const show_content_button_selector =".show_content_button";
const finish_education_button_selector ="#finish_education_button";

const activate_button = $("#activate_button");
const deactivate_button = $("#deactivate_button");
const save_result_note_button = $("#save_result_note_button");

const resultNoteForm = $("#resultNoteForm")

const semester_dropdowns_selector = ".toggle-semester-table";

const turkish_content = $("#turkish-content");

const educationClassContentModal = $("#educationClassContentModal");


const cleanOptions = function (select_input , callback=null) {
  select_input.find("option").each(function () {
    $(this).removeAttr("selected");
    $(this).removeAttr("data-select2-id");
    if ($(this).val()) {
      $(this).remove();
    }
  });

  if (callback) {
    callback();
  }
};
const fillOptions = function (select_input, data, callback = null) {
  // get already selected value
  // to select it with new option list

  cleanOptions(select_input);


  for (option of data) {
    $(select_input).append($('<option>', {
      value: option.id,
      text: option.name
    }));
  }
  if (callback) {
    callback();
  }
};

// Variables
var table = $("#class-datatable");

init();

function init() {
  setupListeners();
  initializeStudentClassDatatables(table, student_classes_list_api_url, education_id)
}

function clearAddClassForm() {
  $("#addClassForm input").val(''); 
  $("#addClassForm textarea").val(''); 
  $("#addClassForm select").val(''); 
  add_class_button.html("Ders Ekle");
  add_class_modal_label.html("Ders Ekle");
}

function getSelectionText() {
  if (window.getSelection) {
    try {
      var activeElement = document.activeElement;
      if (activeElement && activeElement.value) {
        // firefox bug https://bugzilla.mozilla.org/show_bug.cgi?id=85686
        return activeElement.value.substring(activeElement.selectionStart, activeElement.selectionEnd);
      } else {
        return window.getSelection().toString();
      }

    } catch (e) {}
  } else if (document.selection && document.selection.type != "Control") {
    // For IE
    return document.selection.createRange().text;
  }
}

function setupListeners() {
  save_result_note_button.click(function (event) {
    resultNoteForm.submit();
  });
  resultNoteForm.submit(function name(event) {
    event.preventDefault();
    let formData = new FormData(this);
    let data = Object.fromEntries(formData.entries());
    Updateeducation(data, education_closed_api_url, save_result_note_button);
  });
}


//jQuery events


$('tbody').on("click", '.compare_class_button', function (event) {
  let row = $(this).closest("tr");
  let data = table.row(row).data();
  if (data){
    FillDataCompareClassModal(data);
  }
  
});

$('tbody').on("click", '.confirm_class_button', function (event) {
  let row = $(this).closest("tr");
  let data = table.row(row).data();
  if (data){
    confirm_data = { 'education_class': data.education_class.id, 'education': data.education };
    addeducationClassConfirmation(data.id, confirm_data, education_class_confirmation_api_url, $(this), table);
  }
  
});

$('tbody').on("click", '.disconfirm_class_button', function (event) {
  let deleteable_class_id = $(this).data('id');
  if (deleteable_class_id){
    deleteeducationClassConfirmation(deleteable_class_id, education_class_confirmation_delete_api_url, $(this), table);
  }
  
});

$(activate_button).on("click", function(){
  sweetCombineDynamic(
    "Emin misin?",
    "Bu intibak başvurusunu açmak ve tüm derslerin onaylarını silmek istediğine emin misin!",
    "success",
    "Başvuruyu aç.",
    "İptal et.",
    () =>{
    data = { 'is_closed': false };
    Updateeducation(data, education_closed_api_url, $(this), table);
    }
  );
});

$(deactivate_button).on("click", function(){
  data = { 'is_closed': true };
  Updateeducation(data, education_closed_api_url, $(this)); 
});

$(semester_dropdowns_selector).on("click", function(){
  let semester = $(this).data("semester");
  semesterTable = $(`#semester-table-${semester}`);
  semesterTable.slideToggle();
});

$(show_content_button_selector).on("click", function(){
  let id = $(this).data("id");
  geteducationClassContent(id, education_class_detail_api_url, educationClassContentModal)
});


function Updateeducation(_data, _url, _button = null, _table = null, _modal = null) {
  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .patch_r(_url.replace("0", education_id), _data).then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
          if (data.is_closed !== undefined) isClosedButtonControl(data.is_closed);        
          if (_table) {
            _table.ajax.reload()
          }
          fire_alert([{
            message: {message:"Kaydınız başarıyla güncellendi"},
            icon: "success"
          }]);
          if (_modal) {
            _modal.modal('hide');
          }
        })
      } else {
        response.json().then(errors => {
          console.log(errors);
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}


//Classes Activies
function initializeStudentClassDatatables(_table, _student_classes_list_api_url, _education_id) {
  $.extend($.fn.dataTable.defaults, {
    autoWidth: false,
    dom: '<"datatable-header"fBl><"datatable-scroll-wrap"t><"datatable-footer"ip>',
    language: {
      search: "<span>Filter:</span> _INPUT_",
      searchPlaceholder: "Type to filter...",
      lengthMenu: "<span>Show:</span> _MENU_",
      paginate: {
        first: "First",
        last: "Last",
        next: $("html").attr("dir") == "rtl" ? "&larr;" : "&rarr;",
        previous: $("html").attr("dir") == "rtl" ? "&rarr;" : "&larr;",
      },
    },
  });
  table = _table.DataTable({
    "searchCols": [
      null,
      {
        "search": _education_id
      },
    ],
    "serverSide": true,
    "ajax": {"url":_student_classes_list_api_url,"dataSrc":""},
    "columns": [
      {
        "data": "code"
      },
      
      {
        "data": "class_name"
      },
      
      {
        "data": "semester"
      },
      {
        "data": "credit"
      },
      
      {
        "data": "akts"
      },
      
      {
        "data": null,
        "render": function ( data, type, row ) {
            return `
            <div class="row">
             <button class='btn btn-primary compare_class_button mx-auto'  data-toggle="modal" data-target="#compareClassModal" data-id="${data.id}">Karşılaştır</button>
            </div>
          `;
        }
      },
      {
        "name":"confirmation",
        "data": "education_class.code",
        "render": function ( data, type, row ) {
          if(row.confirmation.exists)
          return `
          <div class="row">
            <button class='btn disconfirm_class_button p-0 mx-auto' data-id="${row.confirmation.id}" ><i class='text-danger fas fa-times m-1'></i></button>
            <button class='btn confirm_class_button p-0 mx-auto border border-success'  disabled><i class='text-success fas fa-check m-1'></i></button>
          </div>
          `;

          else 
          return `
          <div class="row">
            <button class='btn disconfirm_class_button p-0 mx-auto border border-danger' disabled><i class='text-danger fas fa-times m-1'></i></button>
            <button class='btn confirm_class_button p-0 mx-auto' ><i class='text-success fas fa-check m-1' data-education-class-id="${row.education_class.id}"></i></button>
          </div>
          `;
        }
      },
    ],
    "rowsGroup": [
      "confirmation:name"
    ]
  });
}

function geteducationClassContent(_id, _url, _modal = null) {
  request
    .get_r(_url.replace("0", _id))
    .then((response) => {
      if (response.ok) {
        response.json().then(data => {
          filleducationClassContent(data);
        })
      } else {
        response.json().then(errors => {
          fire_alert([{ message: errors, icon: "error" }]);
        })
        throw new Error('Something went wrong');
      }
    })
}

function filleducationClassContent(_data) {
  turkish_content.html(_data.turkish_content);
}

function addeducationClassConfirmation(_id, _data, _url, _button = null, _table = null, _modal = null) {
  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .post_r(_url.replace("0", _id), _data).then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
          _table.ajax.reload();
          if (_modal) {
            _modal.modal('hide');
          }
        })
      } else {
        response.json().then(errors => {
          console.log(errors);
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}

function deleteeducationClassConfirmation(_id, _url, _button = null, _table = null, _modal = null) {
  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
  .delete_r(_url.replace("0", _id))
    .then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        if (_table) {
          _table.ajax.reload()
        }
      } else {
        response.json().then(errors => {
          console.log(errors);
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}

function FillDataCompareClassModal(_data) {
  _data.grade = Number(_data.grade).toFixed(1);
  $.each( _data, function( key, value ) {     
    $(`.table-compare #id_${key}`).val(value);
  });
  $.each( _data.education_class, function( key, value ) {     
    $(`.table-compare #id_${key}_education_class`).val(value);
  });
  $(`#id_education_class`).val(_data.education_class.id);
}

function isClosedButtonControl(is_closed) {
  deactivate_button.prop("disabled", is_closed);
  activate_button.prop("disabled", !(is_closed));
}
