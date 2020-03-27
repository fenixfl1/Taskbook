from . import auth_view
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from flask_security import user_registered
from flask_security.datastore import UserDatastore
from werkzeug.utils import secure_filename
from datetime import datetime
from .forms import LoadForm, TaskForm, EventForm, SubjectsForm, ProfeForm, AssingForm
from app.database import db
from app.database.queries import Queries
from app.database.models import ProfilePicture, Tarea, DetalleTarea, Materias, Profesor, User
from config.default import IMAGE_SET_EXT, UPLOAD_FOLDER_DEST
import os
import json


def allowed_image(filename):

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in IMAGE_SET_EXT


# function to upload profile image
@auth_view.route('/uploads', methods=['GET', 'POST'])
@login_required
def Uploads():

    form = LoadForm()

    if form.validate_on_submit():

        picture = request.files['picture']

        if 'picture' not in request.files:
            messages = 'Ninguna imagen seleccionada!'
            category = 'error'
            
            return redirect(request.url)

        if picture.filename == '':
            messages = 'Ninguna imagen selecionada!'
            category = 'error'
            
            return redirect(request.url)

        if picture and allowed_image(picture.filename):
            filename = secure_filename(picture.filename)

            try:

                picture_url = (UPLOAD_FOLDER_DEST)
                _picture = ProfilePicture(picture_url=picture_url,
                                          user_id=current_user.id,
                                          name=filename)

                picture.save(os.path.join(UPLOAD_FOLDER_DEST, filename))

                db.add(_picture)
                db.commit()
                
                messages = 'Imagen guardada con exito!'
                category = 'success'

            except Exception as e:
                messages = 'Ha ocurrido un error.'
                category='error'
                raise e

        else:
            messages = 'Formato de imagen no permintida!'
            category='error'
            
    flash(messages, category)

    return redirect(url_for('users.profile'))
    
    
# function for register subjects
@auth_view.route('/register-subjects', methods=['POST'])
def register_subjects():
    
    form = SubjectsForm()
    
    if form.validate_on_submit():
        
        name = form.name.data
        
        user = Materias(name=name,
                user_id=current_user.id)
        
        try:
            db.add(user)
            db.commit()
            
            messages = 'Asignatura registrada con exito!'
            category = 'success'
            
        except:
            messages = '{0} ya fue registrada!'.format(name)
            category = 'error'
    
    flash(messages, category)
    return redirect(url_for('users.subjects'))


# function to assing teacher to subjects
@auth_view.route('/assing-teacher', methods=['POST'])
def assing_teacher():
    
    form = AssingForm()
    
    id = form.profe.data
    print('Esto es lo que Busco:', id)
    
    if form.validate_on_submit():
        
        profe = db.query(Profesor).filter(Profesor.id==id)
                
        db.query(Materias).filter(Materias.user_id==current_user.id).\
            update({Materias.profesor: profe}, synchronize_session=False)
        
    
    return redirect(url_for('users.subjects'))


# this function is to register new teacher for the current user
@auth_view.route('/register-profesor', methods=['POST'])
def register_profesor():
    
    form = ProfeForm()
    
    if form.validate_on_submit():
        
        user = Profesor(name=form.name.data,
                        materia=form.subjects.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        phone_number=form.phone.data,
                        user_id=current_user.id)
        
        try:
            
            db.add(user)
            db.commit()
            
            messages = 'Registro guardado con exito!'
            category = 'success'
        except:
            
            messages = '{0} ya esta en tu lista de Profesores!'.format(form.name.data)
            category = 'error'    
    
    flash(messages, category)
    return redirect(url_for('users.subjects'))


# this function is to authenticate task and task-details
@auth_view.route('/register_task', methods=['POST'])
def register_task():

    form = TaskForm()

    if form.validate_on_submit():

        task = form.name.data
        materia = form.materia.data
        asignada_en = form.asignada_en.data
        dia_entrega = form.dia_entrega.data
        comentario = form.nota.data
        
        task_id = Queries.queries(Tarea, current_user, order_by='id')
        
        task = Tarea(name=task, user_id=current_user.id)
        db.add(task)
        db.commit()

        try:
            
            id = Queries.get_query(Tarea, current_user)
            
            task_detail = DetalleTarea(
                tarea=task,
                materia=materia,
                asignada_en=asignada_en,
                dia_endrega=dia_entrega,
                comentario=comentario
            )

            db.add(task_detail)
            db.commit()
            message = 'Tarea guardada con exito!'
            category = 'success'

        except:
            db.delete(task)
            messages = 'No fue posible guardar los cambios!'
            category = 'error'

        flash(messages, category)
        return redirect(url_for('users.tasks'))
    
    
# this function is to authenticate events and events-details
@auth_view.route('/register-event', methods=['POST'])
def register_event():
    
    form = EventForm()
    
    if form.validate_on_submit():
        
        pass
    
    return redirect(url_for('users.events'))
    
 
# this function is to delete records in any antity   
@auth_view.route('/delete/<string:id>')
def delete(id):
    
    task = db.query(Tarea).filter(Tarea.user_id==current_user.id).\
        filter(Tarea.id==id).one()
        
    try:
            
        db.delete(task)
        db.commit()
        
        messages = 'Registro eliminado con exito!'
        category='success'
    
    except:
        messages = 'No fue posible eliminar el registro!'
        category='error'
    
    flash(messages, category)
    
    return redirect(url_for('users.tasks'))


# this function is to obtain the datas of the entity you want edit
@auth_view.route('/edit/<string:id>')
def get_edit(id):
    
    return render_template(
        'auth/edit.html.j2',
        title='edit-{}'.format(id)
    )


# this function edit any entity selected in the previus function
@auth_view.route('/edit/<string:id>')
def edit(id):
    
    try:
        task = db.query(Tarea).filter(Tarea.user_id==current_user.id).\
            filter(Tarea.id==id)
            
        task.id = id
        db.commit()
        
        flash('Registro modificado con exito!', category='success')
    
    except:
    
        flash('No fue posible modificar los datos!', category='danger')
        
    return redirect(url_for('users.tasks'))

@auth_view.route('/ajax-login', methods=['GET', 'POST'])
def ajax_login():
    
    print(request.form)
    name = request.form['username']
    
    user = User.get_by_name(name)
    id = User.get_by_id(user.id)
    
    response = {
        'status': 200,
        'username': user,
        'id': id
    }
    
    return json.dumps(response)
