// Assigning Elements
const request = new Request(csrfToken);

var table = $("#class-datatable");
init();

function init() {
  setupListeners();
  initializeeducationDatatables(table, lesson_list_api_url);
}

function initializeeducationDatatables(_table, _lesson_list_api_url) {
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
    serverSide: true,
    ajax: { url: _lesson_list_api_url, dataSrc: "" },
    columns: [
      { data: "code" },
      { data: "class_name" },
      { data: "link" },
      { data: "semester_humanize" },
      { data: "teacher.namesurname" },
      { data: "teacher.user.email" },
      { data: "teacher.user.username" },
      { data: "teacher.phone_number" },
      { data: "teacher.number" },
    ],
  });
}


function setupListeners() {
}