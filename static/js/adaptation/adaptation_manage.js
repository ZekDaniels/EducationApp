// Assigning Elements
const request = new Request(csrfToken);

const university_input = $("#id_university");
const faculty_input = $("#id_faculty");
const science_input = $("#id_science");
const mainForm = $("#mainForm")
const addClassForm = $("#addClassForm")
const main_submit_button = $("#main_submit_button");
const add_class_button = $("#add_class_button");

const table = $(".table");

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

init();

function init() {
  setupListeners();
  initializeStudentClassDatatables(table, student_class_create_api_url)
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

function updateFaculties() {
  new_value = getSelectionText(university_input)
  if (!new_value) {
    cleanOptions(faculty_input);
  } else {
    urlParams = new URLSearchParams();
    urlParams.set("university", new_value);
    faculty_list_api_url.search = urlParams;
    fetch(faculty_list_api_url)
      .then((response) => response.json())
      .then((data) => fillOptions(faculty_input, data, cleanOptions(science_input)))
  }
}

function updateSciences() {
  new_value = getSelectionText(university_input)
  new_value_faculty = getSelectionText(faculty_input)
  if (!new_value) {
    cleanOptions(science_input);
  } else {
    urlParams = new URLSearchParams();
    urlParams.set("faculty", new_value);
    science_list_api_url.search = urlParams;
    fetch(science_list_api_url)
      .then((response) => response.json())
      .then((data) => fillOptions(science_input, data))
  }
}

function setupListeners() {
  university_input.change(() => {
    updateFaculties();
  });
  faculty_input.change(() => {
    updateSciences();
  });
  main_submit_button.click(function (event) {
    mainForm.submit();
  });
  add_class_button.click(function (event) {
    addClassForm.submit();
  });
  mainForm.submit(function name(event) {
    event.preventDefault();
    let formData = new FormData(this);
    let data = Object.fromEntries(formData.entries());
    UpdateAdaptation(data, adaptation_update_api_url, main_submit_button);
  });
  addClassForm.submit(function name(event) {
    event.preventDefault();
    let formData = new FormData(this);
    let data = Object.fromEntries(formData.entries());
    addStudentClass(data, student_class_create_api_url, add_class_button);
  });
}

function UpdateAdaptation(_data, _url, _button = null, _modal = null,  _table = null) {
  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .put_r(_url.replace("0", adaptation_id), _data).then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
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

function addStudentClass(_data, _url, _button = null, _modal = null,  _table = null) {

  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .post_r(_url, _data).then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
          console.log(data);
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

function initializeStudentClassDatatables(_table, _student_class_list_api_url) {
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
  _table.DataTable({
    // "searchCols": [
    //   null,
    //   {
    //     "search": _adaptation_id
    //   },
    // ],
    "serverSide": true,
    "ajax": _student_class_list_api_url,
    "columns": [
      {
        "data": "id"
      },
      {
        "data": "quotation.id"
      },
     
    ],
      "columnDefs": [
      // {
      //   searchable: false,
      //   targets: [7, 9, 11, 12],
      // },
      {
        searchable: false,
        targets: [3],
      },
      {
        "targets": [8, 9],
        data: null,
        createdCell: function (td, cellData, rowData, row, col) {
          $(td).css('width', '125px');
        }
      },
      {
        "targets": 13,
        "data": null,
        className: 'align-center',
        createdCell: function (td, cellData, rowData, row, col) {
          $(td).css('white-space', 'nowrap');
        },
        defaultContent:
          `
        <button class='partCompare btn p-0 mx-1'><i class='text-yellow icon-git-compare'></i></button>
        <button class='partAddNote btn p-0 mx-1'><i class='text-muted icon-notebook'></i></button>
        <button class='partUpdate btn p-0 mx-1'><i class='text-success icon-checkmark3'></i></button>
        <button class='partDelete btn p-0 mx-1'><i class='text-danger fas fa-trash'></i></button>`
      },
      {
        targets: [0, 1, 2],
        className: "d-none"
      }
    ]
  });
}


// function buildClassesTable(data) {
//   const table_body_selector = ".table tbody";
//   const counter_cell_selector = "td.counter_cell";
//   const table_row_selector = `${table_body_selector} tr`;
//   const row_count = $(table_row_selector).length;
//   const last_student_class_row_selector = `${table_row_selector}.${data.adaptation_class_data.code}:last`;
//   const adaptation_class_selector = `${table_row_selector}.${data.adaptation_class_data.code}.adaptation_row`;
  
//   let counter = 0;
//   if(row_count){
//     counter = $(`${last_student_class_row_selector} ${counter_cell_selector}`).html();
//     console.log(counter);
//   }
//   counter++;
//   console.log(adaptation_class_selector);
//   const default_adaptation_cells =`
//   <td rowspan="2" class="align-middle m-auto" >${data.adaptation_class_data.code}</td>
//   <td rowspan="2" class="align-middle m-auto" >${data.adaptation_class_data.class_name}</td>
//   <td rowspan="2" class="align-middle m-auto" >${data.adaptation_class_data.semester}</td>
//   <td rowspan="2" class="align-middle m-auto" >${data.adaptation_class_data.credit}</td>
//   <td rowspan="2" class="align-middle m-auto" >${data.adaptation_class_data.akts}</td>     
//   <td rowspan="2" class="align-middle m-auto" >${data.adaptation_class_data.akts}</td> 
//   `
//   const default_student_row = `
//   <tr class="text-center ${data.adaptation_class_data.code} ${!adaptation_class_selector.length ? 'adaptation_row':''}">
//   <td class="align-middle">${counter}</td>
//   <td class="align-middle">${data.code}</td>
//   <td class="align-middle">${data.class_name}</td>
//   <td class="align-middle">${data.semester}</td>
//   <td class="align-middle">${data.credit}</td>
//   <td class="align-middle">${data.akts}</td>
//   ${!adaptation_class_selector.length ? default_adaptation_cells:''}
//   ${!row_count ? default_adaptation_cells:''}
//   </tr>
//   `

//   if(row_count) $(last_student_class_row_selector).after(default_student_row);
//   else $(table_body_selector).html(default_student_row);                                        
 
  
// }