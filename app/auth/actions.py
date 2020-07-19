from . import auth_view
from flask import redirect, url_for, flash, request
from app.database import db
from app.database.models import StudyPlanGoals as spg
from app.database.models import StudyPlan
from flask_security import login_required


############################################################################
# ------------------ Actions for study plans goals -------------------------
############################################################################
@auth_view.route('/delete_staty_plan_goals/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_plan(id):

    try:
        user = db.query(spg).get(id)
        user.state = 0
        db.commit()

        messages = "Registro eliminado con exitosamente!"
        category = "success"
    except Exception as e:
        raise e
        messages = "Ha ocurrido un error desconocido!"
        category = "error"
    finally:
        flash(messages, category)

    plan_id = request.args.get('plan_id')

    return redirect(url_for('users.study_plan_goals', id=plan_id))


@auth_view.route('/staty_plan_goals/<int:id>/marck_as_done')
@login_required
def marck_as_done(id):

    try:
        user = db.query(spg).get(id)
        user.done = 1

        db.commit()

        messages = "Has completado un nuevo objetivo!"
        category = "success"

    except Exception as e:
        raise e

        messages = "Ha ocurrido un error desconocido!"
        category = "error"

    finally:
        flash(messages, category)

    plan_id = request.args.get('plan_id')

    return redirect(url_for('users.study_plan_goals', id=plan_id))


############################################################################
# ------------------------ Actions for study plans  ------------------------
############################################################################
@auth_view.route('/staty_plan/edit', methods=['POST'])
@login_required
def staty_plan_edit():

    messages = ""
    category = ""

    form = request.form

    try:
        user = db.query(StudyPlan).get(form.get('id'))
        # user.one()

        user.name = form.get('name')
        user.start_date = form.get('start_date')

        db.commit()

        messages = "La informacion fue editada exitosamente!"
        category = "success"

    except ValueError as e:
        raise e

        messages = "Ha ocurrido un error desconocido!"
        category = "error"

    finally:
        flash(messages, category)

    return redirect(url_for('users.plan_de_estudio'))
