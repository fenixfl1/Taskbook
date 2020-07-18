from . import auth_view
from flask import redirect, url_for, flash, request
from app.database import db
from app.database.models import StudyPlanGoals as spg
from flask_security import login_required


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

    return redirect(url_for('users.study_plan_golas', id=plan_id))
