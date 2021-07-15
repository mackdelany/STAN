
from datetime import datetime
from time import sleep
import traceback
from typing import Union

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, StatementError, IntegrityError

from ..core.triage_request import TriageRequest, TriageRequestTuple, tr_dict_to_named_tuple
from .models import db, Hospital, DHB, TriageEvent, PresentingComplaint


class STANDatabase():
    def __init__(
        self,
        db,
        dhb_table: db.Model,
        hospital_table: db.Model,
        pc_table: db.Model,
        triage_event_table: db.Model,
        cache_tables: bool = True,
        request_retry_count: int = 3
        ) -> None:
        """
        """
        self.db = db
        self.dhb_table = dhb_table
        self.hospital_table = hospital_table
        self.pc_table = pc_table
        self.triage_event_table = triage_event_table
        self.request_retry_count = request_retry_count
        if cache_tables:
            self._cache_tables()

    def _cache_tables(self):
        """
        """
        #TODO implement
        pass

    def handle_request(
        self,
        triage_request: Union[TriageRequest, dict], 
        stan_code: float,
        model_code: float
        ) -> None:
        """
        """
        if isinstance(triage_request, TriageRequest):
            triage_request = triage_request.get_triage_event_dict()
        if isinstance(triage_request, dict): # celery worker changes namedtuple input to dict
            triage_request = tr_dict_to_named_tuple(triage_request)
        self._log_request(triage_request, stan_code, model_code)

    def _log_request(
        self,
        triage_request: TriageRequestTuple, 
        stan_code: float,
        model_code: float,
        attempt: int = 0
        ) -> None:
        """
        """
        #TODO retry logic?
        # retrying query: https://stackoverflow.com/questions/53287215/retry-failed-sqlalchemy-queries
        #TODO add session rollback for invalid transactions
        # https://stackoverflow.com/questions/41086632/aiohttpsqlalchemy-cant-reconnect-until-invalid-transaction-is-rolled-back

        while attempt < self.request_retry_count:
            sleep_time = (2 ** attempt) - 1
            if sleep_time:
                print('Attempt {}, sleeping for {}s'.format(attempt, sleep_time))
                sleep(sleep_time)
            try:
                hospital_id = self._get_hospital_id(
                    triage_request.hospital,
                    )
                dhb_id = self._get_dhb_id(
                    triage_request.dhb
                    )
                event_id = self._create_unique_event_id(
                    triage_request.event_id,
                    hospital_id
                    )
                self._check_presenting_complaint(
                    triage_request.presenting_complaint,
                    triage_request.presenting_complaint_group
                    )
                triage_event_model = self._create_triage_event_model(
                    hospital_id,
                    dhb_id,
                    event_id,
                    triage_request,
                    model_code,
                    stan_code
                    )
                db.session.add(triage_event_model)
                db.session.commit()
                break

            except OperationalError as ex:
                print('OperationalError on attempt {}'.format(attempt))
                attempt += 1
                continue

            except IntegrityError as ex:
                print('StatementError on attempt {}'.format(attempt))
                print(str(ex))
                db.session.rollback()
                attempt += 1

            except StatementError as ex:
                print('StatementError on attempt {}'.format(attempt))
                print(str(ex))
                db.session.rollback()
                attempt += 1

            except Exception as ex:
                print('Unknown error\n{}\nRetrying...'.format(str(ex)))
                attempt += 1


    def _get_hospital_id(self, hospital) -> int:
        """
        """
        #TODO cache this ?
        hospital_query = self.hospital_table.query.filter_by(
            hospital=hospital
            ).first()
        if hospital_query:
            # hospital exists, proceed
            hospital_id = hospital_query.id
        else:
            # hospital exist.. create new
            hospital_model = Hospital(
                hospital = str(hospital)
            )
            self.db.session.add(hospital_model)
            self.db.session.commit()
            hospital_id = hospital_model.id
        return hospital_id

    def _get_dhb_id(self, dhb) -> int:
        """
        """
        #TODO cache this ?
        dhb_query = self.dhb_table.query.filter_by(dhb=dhb).first()
        if dhb_query:
            # dhb id exists
            dhb_id = dhb_query.id 
        else :
            # dhb id doesn't exist
            dhb_model = DHB(
                dhb = str(dhb)
                )
            self.db.session.add(dhb_model)
            self.db.session.commit()
            dhb_id = dhb_model.id
        return dhb_id

    @staticmethod
    def _create_unique_event_id(event_id: str, hospital_id: int) -> Union[str, None]:
        """
        """
        if event_id:
            hosp_unique_id = '{}_{}'.format(hospital_id, event_id)
            return hosp_unique_id
        return None

    def _check_presenting_complaint(
        self, 
        presenting_complaint: str,
        presenting_complaint_group: str
        ) -> None:
        """
        """
        presenting_complaint_query = self.pc_table.query.filter_by(
            presenting_complaint=presenting_complaint
            ).first()
        if presenting_complaint_query:
            #pc exists
            pass
        else :
            presenting_complaint_model = self.pc_table(
                presenting_complaint = str(presenting_complaint),
                presenting_complaint_group = str(presenting_complaint_group)
                )
            db.session.add(presenting_complaint_model)
            db.session.flush()

    def _create_triage_event_model(
        self,
        hospital_id: int,
        dhb_id: int,
        event_id: str,
        triage_request: TriageRequestTuple,
        model_code: float,
        stan_code: float
        ) -> db.Model:
        """
        """
        triage_event_model = self.triage_event_table(
            event_id = event_id,
            method = triage_request.method,
            hospital_id = hospital_id,
            dhb_id = dhb_id,
            present_date_time = triage_request.present_date_time,
            dob = triage_request.dob,
            gender = triage_request.gender,
            presenting_complaint = triage_request.presenting_complaint,
            triage_assessment = triage_request.triage_assessment,
            nurse_triage_code = triage_request.nurse_triage_code,
            stan_model_code = model_code,
            stan_triage_code = stan_code,
            vital_signs_pulse = triage_request.vital_signs_pulse,
            respiratory_rate = triage_request.respiratory_rate,
            temperature = triage_request.temperature,
            blood_pressure_systolic = triage_request.blood_pressure_systolic,
            blood_pressure_diastolic = triage_request.blood_pressure_diastolic,
            sats = triage_request.sats,
            airway_altered = triage_request.airway_altered,
            breathing_altered = triage_request.breathing_altered,
            circulation_altered = triage_request.circulation_altered,
            disability_gcs = triage_request.disability_gcs,
            pain_scale = triage_request.pain_scale,
            neuro_altered = triage_request.neuro_altered,
            mental_health_concerns = triage_request.mental_health_concerns,
            immunocompromised = triage_request.immunocompromised,
            vital_signs_pulse_was_measured = triage_request.vital_signs_pulse_was_measured,
            respiratory_rate_was_measured = triage_request.respiratory_rate_was_measured,
            temperature_was_measured = triage_request.temperature_was_measured,
            blood_pressure_was_measured = triage_request.blood_pressure_was_measured,
            sats_was_measured = triage_request.sats_was_measured,
            airway_was_measured = triage_request.airway_was_measured,
            breathing_was_measured = triage_request.breathing_was_measured,
            circulation_was_measured = triage_request.circulation_was_measured,
            disability_gcs_was_measured = triage_request.disability_gcs_was_measured,
            pain_was_measured = triage_request.pain_was_measured,
            neuro_was_measured = triage_request.neuro_was_measured,
            mental_health_was_measured = triage_request.mental_health_was_measured,
            immunocompromised_was_measured = triage_request.immunocompromised_was_measured,
            )
        return triage_event_model