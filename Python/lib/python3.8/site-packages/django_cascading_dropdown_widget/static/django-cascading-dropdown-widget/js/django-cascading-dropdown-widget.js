(function($){
    $.fn.django_cascading_dropdown_widget = function(){
        return this.each(function(){
            $(this).find(".django-cascading-dropdown-widget-select").change(function(){
                var value = $(this).val();
                var name = $(this).attr("data-name");
                var show_name = name + "-" + value;
                var input = $(this).prevAll(".django-cascading-dropdown-widget-hidden-input");
                $(this).nextAll().hide();
                var next_select = $(this).nextAll(".django-cascading-dropdown-widget-select[data-name=" + show_name + "]");
                if(next_select.length > 0){
                    next_select.show();
                    input.val("").change();
                }else{
                    input.val(value).change();
                }
            });
        });
    };
    $(document).arrive(".django-cascading-dropdown-widget", {
        existing: true
    }, function(){
        $(this).django_cascading_dropdown_widget();
    });
})(jQuery);
