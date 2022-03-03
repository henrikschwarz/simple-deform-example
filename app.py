from flask import render_template, Flask, jsonify, request
# forms are stored in the forms folder


#Creating the flask "application"
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
## templates reload without "server restart"
app.config['TEMPLATES_AUTO_RELOAD'] = True


from colander import (
    Boolean,
    Integer,
    Length,
    MappingSchema,
    OneOf,
    SchemaNode,
    SequenceSchema,
    String
)

from deform import (
    Form,
    ValidationFailure,
    widget
)

colors = (('red', 'Red'), ('green', 'Green'), ('blue', 'Blue'))

class DateSchema(MappingSchema):
    month = SchemaNode(Integer())
    year = SchemaNode(Integer())
    day = SchemaNode(Integer())

class DatesSchema(SequenceSchema):
    date = DateSchema()

class MySchema(MappingSchema):
    name = SchemaNode(String(),
                      description = 'The name of this thing')
    title = SchemaNode(String(),
                       widget = widget.TextInputWidget(size=40),
                       validator = Length(max=20),
                       description = 'A very short title')
    password = SchemaNode(String(),
                          widget = widget.CheckedPasswordWidget(),
                          validator = Length(min=5))
    is_cool = SchemaNode(Boolean(),
                         default = True)
    dates = DatesSchema()
    color = SchemaNode(String(),
                       widget = widget.RadioChoiceWidget(values=colors),
                       validator = OneOf(('red', 'blue')))



#A standard entry point to be served accepting both GET and POST calls.
@app.route("/", methods=["POST","GET"])
def questions():
    schema = MySchema()
    myform = Form(schema, buttons=('submit',))
    template_values = {}
    template_values.update(myform.get_widget_resources())

    if request.method == "POST":
        data = request.POST.items()
        try:
            myform.validate(request.form.data)
        except ValidationFailure as e:
            template_values['form'] = e.render()
        else:
            template_values['form'] = 'OK'
        return template_values


    return render_template("questions.html", form = myForm.render()) # render the templates/questions.html page
	

if __name__=="__main__":
	app.debug = True;
	app.run(debug=True)