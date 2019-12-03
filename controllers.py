from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from integrations import GoogleCivics
from integrations import Propublica
from forms import AddressForm

bp = Blueprint('civics', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = AddressForm()
    if form.validate_on_submit():
        return redirect(url_for('civics.run',
                                street=form.street.data,
                                city=form.city.data,
                                state=form.state.data,
                                zip=form.zip.data))
    return render_template('submit_address.html', title='Address', form=form)


@bp.route('/reps')
def run():
    street = request.args.get('street')
    city = request.args.get('city')
    state = request.args.get('state')
    zip = request.args.get('zip')
    address = f"{street} {city} {state} {zip}"
    response_dict = GoogleCivics.get_reps_by_zip(address)
    return render_template('reps.html', title=f'Reps for {address}', response_obj=response_dict)


@bp.route('/elections')
def get_elections():
    response_dict = GoogleCivics.get_elections()
    return render_template('elections.html', title='Upcoming Elections', response_obj=response_dict)


@bp.route('/senators')
def get_senators():
    response_dict = Propublica.get_senate_members()
    return render_template('national_senate.html', title='US Senators', response_obj=response_dict)
