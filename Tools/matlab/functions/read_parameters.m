function params = read_parameters(filename)
    % readParams - Reads simulation parameters from a .in file into a struct
    %
    % Syntax: params = readParams('parameters.in')

    fid = fopen(filename, 'r');
    if fid == -1
        error('Could not open file: %s', filename);
    end

    try
        % Helper to read next line and extract numeric values as a column vector
        getNext = @(fid) sscanf(fgetl(fid), '%f');

        % Line 1: Lx, Ly
        L = getNext(fid);
        params.Lx = L(1);
        params.Ly = L(2);

        % Line 2: Np
        params.Np = getNext(fid);

        % Line 3: total_steps
        params.total_steps = getNext(fid);

        % Line 4: save_interval
        params.save_interval = getNext(fid);

        % Line 5: stats interval
        params.stats_interval = getNext(fid);

        % Line 6: dt
        params.dt = getNext(fid);

        % Line 7: Field Params (M, D, tau, u)
        fParams = getNext(fid);
        params.M    = fParams(1);
        params.D    = fParams(2);
        params.tau  = fParams(3);
        params.u    = fParams(4);

        % Line 8: mean psi
        params.mean_psi = getNext(fid);

        % Line 9: Coupling
        coupling = getNext(fid);
        params.coupling = coupling';

        % Line 10: Reff
        params.Reff = getNext(fid);

        % Line 11: WCA
        wca = getNext(fid);
        params.wca = wca';

        % Line 12: temp
        params.temp = getNext(fid);

        % Line 13: Gammas
        gammas = getNext(fid);
        params.gammas = gammas';

        % Line 14: vact
        params.vact = getNext(fid);

        % Line 15: noise strength
        params.noise_strength = getNext(fid);

        % Line 16: custom initial condition
        line16 = fgetl(fid);
        params.custom_init = contains(lower(line16), 'true');

    catch ME
        fclose(fid);
        rethrow(ME);
    end

    fclose(fid);
end