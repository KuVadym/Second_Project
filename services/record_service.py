from schemas.record_schema import RecordAuth
from models.models_mongo import Emails, Phones, Records


class RecordService:
    print('here')
 

    @staticmethod
    async def create_record(record: RecordAuth):
        async def create_phone(record: RecordAuth):
            phone_list = []
            for phone in record.phones:
                print('/n/n/n')
                print(phone.phone)
                print(type(phone.phone))
                print('/n/n/n')
                phone_list.append(Phones(phone = phone.phone))
            return phone_list
        async def create_email(record: RecordAuth):
            email_list = []
            for email in record.emails:
                email_list.append(Emails(email = email.email))
            return email_list 
        phones,emails = await create_phone(record), await create_email(record)
        print(record.dict())
        print(type(phones))
        print(type(emails))
        # print(type(record.birth_date))
        record_in = Records(
            name = record.name,
            # birth_date = record.birth_date,
            address = record.address,
            phones = phones,
            emails = emails
        )
        return await record_in.save()