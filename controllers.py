from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .integrations import GoogleCivics
from .forms import AddressForm

bp = Blueprint('civics', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = AddressForm()
    if form.validate_on_submit():
        return redirect(url_for('civics.run', zip_code=form.address.data))
    return render_template('submit_address.html', title='Address', form=form)


@bp.route('/<zip_code>')
def run(zip_code):
    reps_object = GoogleCivics.get_reps_by_zip(zip_code)
    return render_template('reps.html', title='Your Reps by Zip Code', reps=reps_object)
