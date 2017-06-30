from __future__ import print_function
from gooey import Gooey
from gooey import GooeyParser
from dkan.client import DatasetAPI


def run(args):
    api = DatasetAPI(args.DkanHost, args.Token)
    if args.Action == 'Create':
        data = {
          'title': args.title,
          'type': args.type
        }
        print ("Attempting to create a new Dataset/Resource...")
        dataset = api.node('create', data=data)
        print("Process Completed: ", dataset.status_code, dataset.text)
    elif args.Action == 'Attach_File':
        print ("Attempting to Upload the file to the Dataset...")
        r = api.attach_file_to_node(args.filename, args.node_id, 'field_upload')
        print("Process Completed: ", r.status_code, r.text)
    elif args.Action == 'Delete':
        print ("Attempting to Delete ...")
        op = api.node('delete', node_id=args.node_id)
        print("Process Completed: ", op.status_code, op.text)
    elif args.Action == 'Update':
        print ("Attempting to Update ...")
        r = api.node('update', node_id=int(args.node_id), data=eval(args.parameters))
        print("Process Completed: ", r.status_code, r.text)
    else:
        print("We only support 'Create', 'Upload', 'Delete' and 'Update'\
              at the moment")

@Gooey(advanced=True)
def main():
    parser = GooeyParser(description="DkanGUI")
    parser.add_argument(
        'DkanHost',
        help="Url of the DKAN Host",
        nargs='?',
        )
    parser.add_argument(
        'Token',
        help="Token to authorize you to DKAN"
        )
    parser.add_argument(
        'Action',
        help="Select the operation you want to perform:",
        choices=['Create', 'Delete', 'Attach_File', 'Update']
    )
    parser.add_argument(
        '--filename',
        help="name of the file to Upload",
        widget='FileChooser',
        required=False,
        )
    parser.add_argument(
        '--title',
        help="Title of the Dataset you will be creating",
        required=False,
        )
    parser.add_argument(
        '--node_id',
        type=int,
        required=False,
        help='Id of the Resource / Node / Dataset you are updating or\
        uploading a file to'
        )
    parser.add_argument(
        '--type',
        help="Select the Type of the Element",
        choices=['dataset', 'resource']
        )
    parser.add_argument(
        '--parameters',
        help="Specify direct and explcit JSON to update",
        type=str,
        required=False
        )

    args = parser.parse_args()
    run(args)


if __name__ == '__main__':
    main()
