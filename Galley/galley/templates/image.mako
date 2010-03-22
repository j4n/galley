<%inherit file="/base.mako"/>\

   <div class='whitebox'>
    <a href="${c.filename}">
     <img src="${h.url('resize', filename='filename', resize='size')}" alt="${c.filename}"/>
    </a>
   </div>

<%doc>
url(controller='content', action='view', id=2)
        other_images = glob(os.path.dirname(image) + "/*.[jJ][pP]*[gG]")
        current_index = other_images.index(image)

        if (current_index > 0):
            previous_index = current_index - 1
            html += """   <div class="to-left navigation"> <a href="%s?view=700">previous</a></div>""" % os.path.basename(other_images[previous_index])

            html += """   <div class="to-center navigation"> <a href="%s">up</a></div>""" % self.split_path_from_item(os.path.dirname(other_images[current_index]))

        if (current_index < ((len(other_images)) - 1)):
            next_index = current_index + 1
            html += """   <div class="to-right navigation"> <a href="%s?view=700">next</a></div>""" % os.path.basename(other_images[next_index])

</%doc>