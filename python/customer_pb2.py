# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: customer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='customer.proto',
  package='banking',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0e\x63ustomer.proto\x12\x07\x62\x61nking\"\'\n\x08WriteSet\x12\x1b\n\x13write_operation_ids\x18\x01 \x03(\x05\"{\n\x0e\x41\x63\x63ountRequest\x12\x12\n\ncustomerId\x18\x01 \x01(\t\x12\x13\n\x06\x61mount\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12(\n\x08writeset\x18\x03 \x01(\x0b\x32\x11.banking.WriteSetH\x01\x88\x01\x01\x42\t\n\x07_amountB\x0b\n\t_writeset\"x\n\x0f\x41\x63\x63ountResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x12\n\x05money\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x1f\n\x12write_operation_id\x18\x03 \x01(\x05H\x01\x88\x01\x01\x42\x08\n\x06_moneyB\x15\n\x13_write_operation_id2\xc8\x01\n\x07\x41\x63\x63ount\x12<\n\x05Query\x12\x17.banking.AccountRequest\x1a\x18.banking.AccountResponse\"\x00\x12>\n\x07\x44\x65posit\x12\x17.banking.AccountRequest\x1a\x18.banking.AccountResponse\"\x00\x12?\n\x08Withdraw\x12\x17.banking.AccountRequest\x1a\x18.banking.AccountResponse\"\x00\x62\x06proto3'
)




_WRITESET = _descriptor.Descriptor(
  name='WriteSet',
  full_name='banking.WriteSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='write_operation_ids', full_name='banking.WriteSet.write_operation_ids', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=66,
)


_ACCOUNTREQUEST = _descriptor.Descriptor(
  name='AccountRequest',
  full_name='banking.AccountRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='customerId', full_name='banking.AccountRequest.customerId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='amount', full_name='banking.AccountRequest.amount', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='writeset', full_name='banking.AccountRequest.writeset', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_amount', full_name='banking.AccountRequest._amount',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_writeset', full_name='banking.AccountRequest._writeset',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=68,
  serialized_end=191,
)


_ACCOUNTRESPONSE = _descriptor.Descriptor(
  name='AccountResponse',
  full_name='banking.AccountResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='banking.AccountResponse.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='money', full_name='banking.AccountResponse.money', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='write_operation_id', full_name='banking.AccountResponse.write_operation_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_money', full_name='banking.AccountResponse._money',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_write_operation_id', full_name='banking.AccountResponse._write_operation_id',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=193,
  serialized_end=313,
)

_ACCOUNTREQUEST.fields_by_name['writeset'].message_type = _WRITESET
_ACCOUNTREQUEST.oneofs_by_name['_amount'].fields.append(
  _ACCOUNTREQUEST.fields_by_name['amount'])
_ACCOUNTREQUEST.fields_by_name['amount'].containing_oneof = _ACCOUNTREQUEST.oneofs_by_name['_amount']
_ACCOUNTREQUEST.oneofs_by_name['_writeset'].fields.append(
  _ACCOUNTREQUEST.fields_by_name['writeset'])
_ACCOUNTREQUEST.fields_by_name['writeset'].containing_oneof = _ACCOUNTREQUEST.oneofs_by_name['_writeset']
_ACCOUNTRESPONSE.oneofs_by_name['_money'].fields.append(
  _ACCOUNTRESPONSE.fields_by_name['money'])
_ACCOUNTRESPONSE.fields_by_name['money'].containing_oneof = _ACCOUNTRESPONSE.oneofs_by_name['_money']
_ACCOUNTRESPONSE.oneofs_by_name['_write_operation_id'].fields.append(
  _ACCOUNTRESPONSE.fields_by_name['write_operation_id'])
_ACCOUNTRESPONSE.fields_by_name['write_operation_id'].containing_oneof = _ACCOUNTRESPONSE.oneofs_by_name['_write_operation_id']
DESCRIPTOR.message_types_by_name['WriteSet'] = _WRITESET
DESCRIPTOR.message_types_by_name['AccountRequest'] = _ACCOUNTREQUEST
DESCRIPTOR.message_types_by_name['AccountResponse'] = _ACCOUNTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WriteSet = _reflection.GeneratedProtocolMessageType('WriteSet', (_message.Message,), {
  'DESCRIPTOR' : _WRITESET,
  '__module__' : 'customer_pb2'
  # @@protoc_insertion_point(class_scope:banking.WriteSet)
  })
_sym_db.RegisterMessage(WriteSet)

AccountRequest = _reflection.GeneratedProtocolMessageType('AccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTREQUEST,
  '__module__' : 'customer_pb2'
  # @@protoc_insertion_point(class_scope:banking.AccountRequest)
  })
_sym_db.RegisterMessage(AccountRequest)

AccountResponse = _reflection.GeneratedProtocolMessageType('AccountResponse', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTRESPONSE,
  '__module__' : 'customer_pb2'
  # @@protoc_insertion_point(class_scope:banking.AccountResponse)
  })
_sym_db.RegisterMessage(AccountResponse)



_ACCOUNT = _descriptor.ServiceDescriptor(
  name='Account',
  full_name='banking.Account',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=316,
  serialized_end=516,
  methods=[
  _descriptor.MethodDescriptor(
    name='Query',
    full_name='banking.Account.Query',
    index=0,
    containing_service=None,
    input_type=_ACCOUNTREQUEST,
    output_type=_ACCOUNTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Deposit',
    full_name='banking.Account.Deposit',
    index=1,
    containing_service=None,
    input_type=_ACCOUNTREQUEST,
    output_type=_ACCOUNTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Withdraw',
    full_name='banking.Account.Withdraw',
    index=2,
    containing_service=None,
    input_type=_ACCOUNTREQUEST,
    output_type=_ACCOUNTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ACCOUNT)

DESCRIPTOR.services_by_name['Account'] = _ACCOUNT

# @@protoc_insertion_point(module_scope)
