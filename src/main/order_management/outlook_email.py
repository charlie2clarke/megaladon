'''Writes emails on a Windows PC using Outlook.

Sends email to specified email address with details on updated order status.
'''
import win32com.client


def update_status(order, products_and_quantities):
    '''Sends email using Outlook with details of order status.

    Args:
        order: instance of Order to notify on status update.
        products_and_quantities: dictionary with product as key and
        quantity as value.

    Raises:
        Exception: an error with using the Outlook client.
    '''
    mail_subject = 'Your order has been ' + order.status.lower()
    recipient_name = order.customer.first_name + \
        ' ' + order.customer.last_name
    ordered_items = ["  " + str(key) + ' * ' + str(
        products_and_quantities[key])
                     for key in products_and_quantities]
    ordered_items = '\n'.join(ordered_items)
    date = order.dispatched_date if order.status == 'Dispatched' else \
        order.completed_date
    mail_body = 'Dear {},\n\n'\
                'Your order of:\n'\
                '{}\n\n'\
                'Was {} on: {}'.format(
                    recipient_name, ordered_items, order.status, date)

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        outlook_msg = outlook.CreateItem(0)
        outlook_msg.To = order.customer.email

        outlook_msg.Subject = mail_subject
        outlook_msg.Body = mail_body

        outlook_msg.Display()
        print("PRINTED")
    except Exception as e:
        print("Error occured trying to open outlook email - this could "
              "be because you have alerts open. More details: " + str(e))
        raise
    return mail_subject, mail_body
