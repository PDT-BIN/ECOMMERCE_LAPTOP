'''
    def load_data():
        from csv import reader
        from random import randint
        # COLUMNS: MODEL NAME, SCREEN, CPU, VGA, RAM, DISK, WEIGHT, OS, BATTERY, PRICE, IMAGE.
        with open('C:/Users/BIN BIN/Desktop/DJANGO PROJECT/resource/data.csv') as csv_file:
            translator = {'V?n ph�ng': 'Văn phòng', 'V?n phï¿½ng': 'Văn phòng', 'Gaming': 'Gaming',
                        'M?ng nh?': 'Mỏng nhẹ', '?? ho?, k? thu?t': 'Đồ họa - Kỹ thuật'}
            for data in reader(csv_file):
                # CREATE SPECIFICATION.
                attrs = {
                    'screensize': float(data[1].split(' - ')[0].strip('"')),
                    'resolution': data[1].split(' - ')[1].strip('"'),
                    'cpu': data[2], 'vga': data[3], 'ram': data[4], 'disk': data[5],
                    'weight': float(data[6].split(' / ')[0].removesuffix(' Kg')),
                    'os': data[7], 'battery': float(data[8].split(' - ')[1].strip(' h'))
                }
                specification, _ = Specification.objects.get_or_create(**attrs)
                # CREATE MANUFACTURER.
                name = data[0].split(' ')[0]
                manufacturer, _ = Manufacturer.objects.get_or_create(name=name)
                # CREATE CATEGORY.
                name = translator[data[11]]
                category, _ = Category.objects.get_or_create(name=name)
                # CREATE MODEL.
                attrs = {
                    'manufacturer': manufacturer, 'specification': specification, 'category': category,
                    'name': data[0].removesuffix(' (US)').strip().replace('  ', ' '),
                    'price': data[9], 'image': data[10], 'quantity': 0
                }
                LaptopModel.objects.create(**attrs)
        # CREATE STATES OF ORDER.
        from orders.models import State
        for name in ('Chờ xác nhận', 'Đang xử lý', 'Đang vận chuyển', 'Đã giao', 'Đã hủy'):
            State.objects.create(name=name)
        # CREATE SUPPLIER.
        for supplier in ('Nguyễn Kim', 'Phong Vũ', 'Thế Giới Di Động', 'FPT Shop', 'Viettel Store'):
            Supplier.objects.create(name=supplier)
'''


'''
    def load_user():
        staff = User.objects.create(username='staff', password='123456', email='staff@gmail.com')
        staff.is_staff = True
        staff.set_password('123456')
        staff.save()
        Employee.objects.create(user=staff, salary=15_000_000)

        shipper = User.objects.create(username='shipper', password='123456', email='shipper@gmail.com')
        shipper.is_shipper = True
        shipper.set_password('123456')
        shipper.save()
        Employee.objects.create(user=shipper, salary=10_000_000)

        customer = User.objects.create(username='customer', password='123456', email='customer@gmail.com')
        customer.set_password('123456')
        customer.is_active = True
        customer.save()
        Customer.objects.create(user=customer)
'''


'''
    def init_data():
        from random import choice, choices, randint
        
        employee = Employee.objects.get(pk=1)
        suppliers = Supplier.objects.all()
        all_models = LaptopModel.objects.all()
        prices = [15_000_000 + i * 5_000_000 for i in range(8)]

        for _ in range(20):
            # CREATE RESERVATION FORM.
            reservation = ReservationForm.objects.create(employee=employee, supplier=choice(suppliers))
            for model in set(choices(all_models, k=10)):
                ReservationDetails.objects.create(
                    reservation_form=reservation, laptop_model=model, quantity=randint(1, 10), price=choice(prices))
            # CREATE IMPORTATION FORM.
            importation = ImportationForm.objects.create(reservation_form=reservation, employee=employee)
            for detail in set(choices(ReservationDetails.objects.filter(reservation_form=reservation), k=5)):
                quantity = randint(1, detail.quantity)
                ImportationDetails.objects.create(
                    importation_form=importation, reservations_detail=detail, quantity=quantity)
                # INCREASE LAPTOP MODEL QUANTITY.
                model = detail.laptop_model
                model.quantity += quantity
                model.save()
                # CREATE LAPTOP OBJECTS OF MODEL.
                for _ in range(quantity):
                    Laptop.objects.create(laptop_model=model, importation_form=importation)
'''
