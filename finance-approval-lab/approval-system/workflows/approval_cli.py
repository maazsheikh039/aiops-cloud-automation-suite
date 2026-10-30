#!/usr/bin/env python3
import sys
import argparse
from approval_engine import ApprovalEngine

def main():
    parser = argparse.ArgumentParser(description='Finance Approval System')
    parser.add_argument('action', choices=['request', 'approve', 'status'])
    parser.add_argument('--request-id', help='Request ID')
    parser.add_argument('--amount', type=float, help='Financial amount')
    parser.add_argument('--requester', help='Requester username')
    parser.add_argument('--approver', help='Approver username')
    parser.add_argument('--description', help='Request description')
    
    args = parser.parse_args()
    engine = ApprovalEngine()
    
    if args.action == 'request':
        if args.amount is None or not args.requester:
            print("Error: --amount and --requester are required for requests.")
            sys.exit(1)
        req_data = {
            "amount": args.amount,
            "requester": args.requester,
            "description": args.description or "No description provided"
        }
        res = engine.request_approval(req_data)
        print("Approval Request Created Successfully:")
        print(json_pretty(res))
        
    elif args.action == 'approve':
        if not args.request_id or not args.approver:
            print("Error: --request-id and --approver are required for approval.")
            sys.exit(1)
        res = engine.approve_request(args.request_id, args.approver)
        print("Approval Action Result:")
        print(json_pretty(res))
        
    elif args.action == 'status':
        if not args.request_id:
            print("Error: --request-id is required to check status.")
            sys.exit(1)
        res = engine.get_request_status(args.request_id)
        print("Request Status Details:")
        print(json_pretty(res))

def json_pretty(data):
    import json
    return json.dumps(data, indent=2)

if __name__ == '__main__':
    main()
