_spman() {
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    subcommands_main="--help --check-version --repolist --repoinfo --blacklist \
        --update --health --new-config --check-upgrade --download"

    subcommands_download="--pkg --src"
    subcommands_repo="alienbob multilib sbo slack"
    subcommands_pkgname="list_pkg_names"

    if [[ ${COMP_CWORD} == 1 ]] ; then
        COMPREPLY=( $(compgen -W "${subcommands_main}" -- ${cur}) )
        return 0
    fi

    case "${COMP_WORDS[1]}" in
        --help)
            COMPREPLY=()
            return 0
            ;;

        --check-version)
            COMPREPLY=()
            return 0
            ;;

        --repolistj)
            COMPREPLY=()
            return 0
            ;;

        --repoinfo)
            COMPREPLY=()
            return 0
            ;;

        --blacklist)
            COMPREPLY=()
            return 0
            ;;

        --update)
            COMPREPLY=()
            return 0
            ;;

        --health)
            COMPREPLY=()
            return 0
            ;;

        --new-config)
            COMPREPLY=()
            return 0
            ;;

        --check-upgrade)
            COMPREPLY=()
            return 0
            ;;

        --download)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=( $(compgen -W "${subcommands_download}" -- ${cur}) )
                return 0
            fi

            if [[ ${COMP_CWORD} == 3 ]] ; then
                COMPREPLY=($(compgen -W "${subcommands_repo}" -- ${cur}))
                return 0
            fi

            if [[ ${COMP_CWORD} == 4 ]] ; then
                COMPREPLY=($(compgen -W "${subcommands_pkgname}" -- ${cur}))
                return 0
            fi
    esac
    return 0
}

complete -F _spman spman

