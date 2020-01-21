from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from integrations import GoogleCivics
from integrations import Propublica
from integrations import SupremeCourt
from integrations.OpenStates import OpenStates
from integrations.Propublica import Propublica
from forms import AddressForm
from forms import StateForm

bp = Blueprint('civics', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = AddressForm()
    if form.validate_on_submit():
        return redirect(url_for('civics.get_reps',
                                street=form.street.data,
                                city=form.city.data,
                                state=form.state.data,
                                zip=form.zip.data))
    return render_template('submit_address.html', title='Address', form=form)


@bp.route('/reps')
def get_reps():
    street = request.args.get('street')
    city = request.args.get('city')
    state = request.args.get('state')
    zip = request.args.get('zip')
    address = f"{street} {city} {state} {zip}"
    response_dict = GoogleCivics.get_reps_by_address(address)
    return render_template('reps.html', title=f'Reps for {address}', response_obj=response_dict)


@bp.route('/elections')
def get_elections():
    response_dict = GoogleCivics.get_elections()
    return render_template('elections.html', title='Upcoming Elections', response_obj=response_dict)


@bp.route('/senators')
def get_senators():
    response_dict = Propublica().get_us_members()
    return render_template('us_gov.html', title='US Senators', response_obj=response_dict)


@bp.route('/submit_state_senators', methods=['GET', 'POST'])
def submit_for_state_senators():
    form = StateForm()
    if form.validate_on_submit():
        return redirect(url_for('civics.get_senators_by_state',
                                state=form.state.data))
    return render_template('submit_state.html', title='State', form=form)


@bp.route('/state_senators')
def get_senators_by_state():
    state = request.args.get('state')
    response_dict = OpenStates().get_state_members(state.lower())
    return render_template('state_gov.html', title=f'Senators for {state}', response_obj=response_dict)


@bp.route('/supreme_court')
def get_supreme_court():
    response_dict = {'justices': SupremeCourt.get_justices()}
    return render_template('supreme_court.html', title=f'Supreme Court', response_obj=response_dict)


@bp.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response
