from dataclasses import dataclass


@dataclass(frozen=True)
class RoleDefinition:
    code: str
    name: str
    description: str


ROLE_ADMINISTRATOR = "administrator"
ROLE_SECRETARY = "secretary"
ROLE_CAREER_COORDINATOR = "career_coordinator"
ROLE_TEACHER = "teacher"
ROLE_STUDENT = "student"
ROLE_ACADEMIC_DIRECTOR = "academic_director"
ROLE_WELLBEING = "wellbeing"
ROLE_LIBRARIAN = "librarian"
ROLE_GUEST = "guest"

ROLE_DEFINITIONS = (
    RoleDefinition(
        ROLE_ADMINISTRATOR,
        "Administrador",
        "Administracion general de usuarios, seguridad y configuracion.",
    ),
    RoleDefinition(
        ROLE_SECRETARY,
        "Secretaria",
        "Operacion academica y gestion parcial de usuarios.",
    ),
    RoleDefinition(
        ROLE_CAREER_COORDINATOR,
        "Coordinador de carrera",
        "Revision academica y consulta de informacion de su carrera.",
    ),
    RoleDefinition(
        ROLE_TEACHER,
        "Docente",
        "Gestion de silabos y notas de cursos asignados.",
    ),
    RoleDefinition(
        ROLE_STUDENT,
        "Estudiante",
        "Consulta de informacion academica propia.",
    ),
    RoleDefinition(
        ROLE_ACADEMIC_DIRECTOR,
        "Direccion academica",
        "Aprobacion y supervision academica institucional.",
    ),
    RoleDefinition(
        ROLE_WELLBEING,
        "Bienestar",
        "Consulta futura para acompanamiento institucional autorizado.",
    ),
    RoleDefinition(
        ROLE_LIBRARIAN,
        "Bibliotecario",
        "Gestion futura de biblioteca y repositorio academico.",
    ),
    RoleDefinition(
        ROLE_GUEST,
        "Invitado/Consulta",
        "Acceso limitado de consulta o auditoria segun autorizacion.",
    ),
)

ROLE_NAME_BY_CODE = {role.code: role.name for role in ROLE_DEFINITIONS}
ROLE_CODE_BY_NAME = {role.name: role.code for role in ROLE_DEFINITIONS}

ACADEMIC_STAFF_ROLES = {
    ROLE_ADMINISTRATOR,
    ROLE_SECRETARY,
    ROLE_CAREER_COORDINATOR,
    ROLE_ACADEMIC_DIRECTOR,
}


def get_user_role_codes(user):
    if not getattr(user, "is_authenticated", False):
        return []

    group_names = user.groups.values_list("name", flat=True)
    return sorted(
        ROLE_CODE_BY_NAME[group_name]
        for group_name in group_names
        if group_name in ROLE_CODE_BY_NAME
    )


def user_has_role(user, *role_codes):
    if getattr(user, "is_superuser", False):
        return True

    user_role_codes = set(get_user_role_codes(user))
    return bool(user_role_codes.intersection(role_codes))
