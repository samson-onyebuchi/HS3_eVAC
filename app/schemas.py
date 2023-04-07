from marshmallow import Schema, fields, validate, validates, ValidationError
import json



class Items(Schema):
    sector = fields.Str(dump_only=True)
    subcategory = fields.Str(required=True)
    hmo = fields.Dict(required=True)


class ItemsUpdates(Schema):
    sector = fields.Str()
    subcategory = fields.Str()
    hmo = fields.Dict()


class SubCatItems(Schema):
    sector = fields.Str(required=True)
    subcategory = fields.Str(required=True)
    name = fields.Str(required=True)
    hmo = fields.Dict(required=True)


class Cards(Schema):
    page_no = fields.Int(required=True)
    print_status = fields.Str(required=True)


class FacilitiesSchema(Schema):
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    lga = fields.Str(dump_only=True)
    ward = fields.Str(dump_only=True)
    type = fields.Str(required=True)
    service = fields.Str(required=True)
    oic_number = fields.Str(required=True, validate=validate.Length(min=11, max=11))


class FacilitiesUpdates(Schema):
    name = fields.Str()
    category = fields.Str()
    lga = fields.Str()
    ward = fields.Str()
    type = fields.Str()
    service = fields.Str()
    oic_number = fields.Str(validate=validate.Length(min=11, max=11))


class Hmoschema(Schema):
    email = fields.Email(required=True)
    phone_number = fields.Str(validate=validate.Length(min=11, max=11))
    name = fields.Str(required=True)


class HmosUpdates(Schema):
    email = fields.Str()
    phone_number = fields.Str(validate=validate.Length(min=11, max=11))
    name = fields.Str()


# class FileUpload(Schema):
#     # file = fields.Raw(metadata={"type": "file","description": "files to attach"})
#     # file = Upload()
#     hmo_name = fields.Str(required=True)
#     hmo_id = fields.Int(required=True)
#     email = fields.Email(required=True)
#     cat_id = fields.Int(required=True)
#     cat_name = fields.Str(required=True)
#     cat = fields.Str(required=True)
#     subcat = fields.Str(required=True)


class AddNom(Schema):
    id_photo = fields.Raw(type="file", required=False)

    category = fields.Str(required=True)
    email = fields.Str(required=True)
    hmo = fields.Str(required=True)
    subcategory = fields.Str(required=True)
    subcategoryitem = fields.Str(required=True)


    @validates('subcategoryitem')
    def is_not_dict(self, value):
        """ make sure fields are a dictionary
        """""
        data = json.loads(value)
        if type(data) != dict:
            raise ValidationError(" this field should be a dictionary")

    @validates('hmo')  #
    def is_not_dict(self, value):
        """ make sure fields are a dictionary
        """""
        data = json.loads(value)
        if type(data) != dict:
            raise ValidationError(" this field should be a dictionary")


class NomUpdates(Schema):
    name = fields.Str()
    date_of_birth = fields.Str()
    gender = fields.Str()
    hmo = fields.Dict()
    subcategoryitem = fields.Dict()
    submission_id = fields.Str(dump_only=True)


class Enrollments(Schema):
    name = fields.Str(required=True)
    date_of_birth = fields.Str(required=True)
    gender = fields.Str(required=True)
    hmo = fields.Str(required=True)
    facility = fields.Str(required=True)
    subcategoryitem = fields.Str(required=True)
    genotype = fields.Str(required=True)
    settlement_type = fields.Str(required=True)
    id_type = fields.Str(required=True)
    lga = fields.Str(required=True)
    ward = fields.Str(required=True)
    home_address = fields.Str(required=True)
    blood_group = fields.Str(required=True)
    nationality = fields.Str(required=True)
    marital_status = fields.Str(required=True)
    email = fields.Str(required=True)
    nin_number = fields.Str(required=True)
    occupation = fields.Str(required=True)
    category = fields.Str(required=True)
    id_photo = fields.Raw(type="file", required=False)
    passport = fields.Raw(type="file", required=False)


    @validates('subcategoryitem') #
    def is_not_dict(self, value):
        """ make sure fields are a dictionary
        """""
        data = json.loads(value)
        if type(data) != dict:
            raise ValidationError(" this field should be a dictionary")

    @validates('hmo')  #
    def is_not_dict(self, value):
        """ make sure fields are a dictionary
        """""
        data = json.loads(value)
        if type(data) != dict:
            raise ValidationError(" this field should be a dictionary")

    @validates('facility')  #
    def is_not_dict(self, value):
        """ make sure fields are a dictionary
        """""
        data = json.loads(value)
        if type(data) != dict:
            raise ValidationError(" this field should be a dictionary")


class Dependent(Enrollments):
    principal_s_submission_id = fields.Str(required=True)
    principals_enrid = fields.Str(required=True)
    dependant_s_phone_number = fields.Str(required=True, validate=validate.Length(max=11))
    type_of_dependent = fields.Str(required=True)
    relationship_with_principal = fields.Str(required=True)
    principal_s_phone_number = fields.Str(required=True, validate=validate.Length(min=11, max=11))


class Principal(Enrollments):
    submission_id = fields.Str(required=True)
    nok_phone = fields.Str(required=True, validate=validate.Length(min=11, max=11))
    phone_number = fields.Str(required=True, validate=validate.Length(min=11, max=11))
    relationship_with_emergency_co = fields.Str(required=True)
    next_of_kin = fields.Str(required=True)
    emergency_contact_address = fields.Str(required=True)
    duration = fields.Str(required=True)


class UpdateEnrollments(Schema):
    name = fields.Str()
    date_of_birth = fields.Str()
    gender = fields.Str()
    hmo = fields.Dict()
    subcategoryitem = fields.Dict()
    submission_id = fields.Str()
    genotype = fields.Str()
    nok_phone = fields.Str(validate=validate.Length(min=11, max=11))
    settlement_type = fields.Str()
    id_type = fields.Str()
    lga = fields.Str()
    ward = fields.Str()
    phone_number = fields.Str(validate=validate.Length(min=11, max=11))
    next_of_kin = fields.Str()
    home_address = fields.Str()
    blood_group = fields.Str()
    relationship_with_emergency_co = fields.Str()
    nationality = fields.Str()
    marital_status = fields.Str()
    email = fields.Str()
    nin_number = fields.Str()
    occupation = fields.Str()
    emergency_contact_address = fields.Str()


class Subscription(Schema):
    name = fields.Str(required=True)
    date_of_birth = fields.Str(required=True)
    gender = fields.Str(required=True)
    enrollment_id = fields.Str(required=True)
    hmo = fields.Dict(required=True)
    subcategoryitem = fields.Dict(required=True)
    facility = fields.Dict(required=True)
    lga = fields.Str(required=True)
    passport = fields.Str(required=True)


class DependentsUpdates(Schema):
    name = fields.Str()
    date_of_birth = fields.Str()
    gender = fields.Str()
    genotype = fields.Str()
    settlement_type = fields.Str()
    id_type = fields.Str()
    lga = fields.Str()
    ward = fields.Str()
    home_address = fields.Str()
    blood_group = fields.Str()
    nationality = fields.Str()
    marital_status = fields.Str()
    email = fields.Str()
    nin_number = fields.Str()
    occupation = fields.Str()


class LimitSkip(Schema):
    limit = fields.Int(required=True)
    skip = fields.Int(required=True)


class DataArgs(LimitSkip):
    download = fields.Str(required=True)


class UpdateWithEnrid(Schema):
    enrollment_id = fields.List(fields.Str(required=True, validate=validate.Length(min=10, max=10)),required=True)


class FileSchema(Schema):
    file = fields.Raw(type="file", required=False)


class Facility(Schema):
    enrollment_id = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    facility_no = fields.Int(required=True)

class Diagnose(Schema):
    diagnosis = fields.Str(required=True)
    facility_no = fields.Int(required=True)


class Serivces(Schema):
    services = fields.List(fields.Dict(required=True), required=True)
    facility_no = fields.Int(required=True)

class Drugs(Schema):
    drugs = fields.List(fields.Dict(required=True), required=True)
    facility_no = fields.Int(required=True)


class EncounterImage(Schema):
    image = fields.Raw(type="file", required=False)
    note = fields.Str(required=True)
    facility_no = fields.Int(required=True)


class Referral(Facility):
    req_services = fields.List(fields.Dict(required=True), required=True)
    note = fields.Str(required=True)
    des_facility = fields.Str(required=True)

class Referrals(Schema):
    req_services = fields.List(fields.Dict(required=True), required=True)
    note = fields.Str(required=True)
    facility_no = fields.Int(required=True)
    encounter_code = fields.Str(required=True, validate=validate.Length(min=8, max=8))
    des_facility = fields.Dict()


class Hmo(Schema):
    hmo_code = fields.Int(required=True)

class Payments(Schema):
    paymentref = fields.Str(required=True)
    channel = fields.Str(required=True)
    duration = fields.Int(required=True)
    transaction_date = fields.Str(required=True)
    transaction_phone = fields.Str(required=True)
    transaction_status = fields.Str(required=True)
    customer_id = fields.Str(required=True)


class HmoAthu(Schema):
    req_services = fields.List(fields.Dict(required=True), required=True)
    note = fields.Str(required=True)
    hmo_code = fields.Int(required=True)
    referral_code = fields.Str(required=True, validate=validate.Length(min=6, max=6))


class QueryFac(Schema):
    query = fields.Str(required=True)
    hmo_code = fields.Int(required=True)
    referral_code = fields.Str(required=True)

class QueryHom(Schema):
    query = fields.Str(required=True)
    referral_code = fields.Str(required=True)


class Signup(Schema):
    role = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    user = fields.Dict()


class Login(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class PRecords(Schema):
    enrollment_id = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    date = fields.Date()



class RefFac(Schema):
    facility_no = fields.Int(required=True)
    referral_code = fields.Str(required=True, validate=validate.Length(min=6, max=6))


class RefRec(Schema):
    referral_code = fields.Str(required=True, validate=validate.Length(min=6, max=6))


class ReferralSec(Schema):
    req_services = fields.List(fields.Dict(required=True), required=True)
    note = fields.Str(required=True)
    facility_no = fields.Int(required=True)
    referral_code = fields.Str(required=True, validate=validate.Length(min=6, max=6))
