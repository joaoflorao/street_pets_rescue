from functools import wraps
from flask import Flask, request, redirect, flash
from sqlalchemy.exc import SQLAlchemyError


def handle_query_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except SQLAlchemyError as e:
            return None
        except Exception as e:
            return None

    return wrapper
